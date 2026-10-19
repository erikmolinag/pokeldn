package org.pokeldn.usbprobe;

import android.hardware.usb.*;
import java.io.IOException;
import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.TimeUnit;

/** The board's serial link: CDC-ACM for native USB, or (poke-app) a Silicon Labs CP210x bridge, which takes
 *  its line settings as vendor requests to its one interface (Silicon Labs AN571) and carries plain bytes. */
public final class UsbStream implements AutoCloseable {
    // CP210x vendor requests, bmRequestType 0x41 (host to device, vendor, interface).
    private static final int CP210X_OUT = 0x41, IFC_ENABLE = 0x00, SET_LINE_CTL = 0x03, SET_MHS = 0x07,
        PURGE = 0x12, SET_BAUDRATE = 0x1e;
    private final UsbDeviceConnection connection;
    private final UsbInterface control, data;
    private final UsbEndpoint input, output;
    private final boolean cp210x;
    private volatile boolean closed;
    private volatile IOException readFailure;
    private final ArrayBlockingQueue<byte[]> incoming = new ArrayBlockingQueue<>(256);
    private Thread reader;
    private Thread writer;
    private volatile boolean queuedWrites;
    private volatile IOException writeFailure;
    private final ArrayBlockingQueue<byte[]> outgoing = new ArrayBlockingQueue<>(1024);
    private final Object writeProgress = new Object();
    private long enqueuedBytes, sentBytes;
    private byte[] remainder = new byte[0];

    public UsbStream(UsbManager manager, UsbDevice device) throws IOException {
        cp210x = Setup.isCp210x(device.getVendorId(), device.getProductId());
        UsbInterface ctl = null, dat = null;
        if (cp210x) {
            if (device.getInterfaceCount() == 0) throw new IOException("Missing CP210x interface");
            ctl = dat = device.getInterface(0);   // one vendor interface: the requests and both bulk pipes
        } else {
            for (int i = 0; i < device.getInterfaceCount(); i++) {
                UsbInterface iface = device.getInterface(i);
                if (iface.getInterfaceClass() == 2) ctl = iface;
                if (iface.getInterfaceClass() == 10) dat = iface;
            }
            if (ctl == null || dat == null) throw new IOException("Missing CDC interfaces");
        }
        control = ctl; data = dat;
        UsbEndpoint in = null, out = null;
        for (int i = 0; i < data.getEndpointCount(); i++) {
            UsbEndpoint endpoint = data.getEndpoint(i);
            if (endpoint.getType() != UsbConstants.USB_ENDPOINT_XFER_BULK) continue;
            if (endpoint.getDirection() == UsbConstants.USB_DIR_IN) in = endpoint;
            else out = endpoint;
        }
        if (in == null || out == null) throw new IOException("Missing bulk endpoints");
        input = in; output = out;
        connection = manager.openDevice(device);
        if (connection == null) throw new IOException("USB open failed");
        try {
            if (cp210x) {
                if (!connection.claimInterface(data, true)) throw new IOException("USB interface claim failed");
                vendor(IFC_ENABLE, 1, null, "CP210x enable");
                vendor(SET_LINE_CTL, 0x0800, null, "CP210x line control");   // 8 data bits, no parity, 1 stop bit
                setBaud(115200);
                vendor(PURGE, 0x000f, null, "CP210x purge");
            } else {
                if (!connection.claimInterface(control, true) || !connection.claimInterface(data, true))
                    throw new IOException("USB interface claim failed");
                byte[] coding = {0, (byte)0xc2, 1, 0, 0, 0, 8};
                if (connection.controlTransfer(0x21, 0x20, 0, control.getId(), coding, 7, 1000) != 7)
                    throw new IOException("CDC line coding failed");
                if (connection.controlTransfer(0x21, 0x22, 0, control.getId(), null, 0, 1000) < 0)
                    throw new IOException("CDC line state failed");
            }
        } catch (IOException error) { close(); throw error; }
        reader = new Thread(this::receiveLoop, "android-usb-reader");
        reader.start();
        writer = new Thread(this::writeLoop, "android-usb-writer");
        writer.start();
    }

    private void receiveLoop() {
        UsbRequest request = new UsbRequest();
        try {
            if (!request.initialize(connection, input)) throw new IOException("USB request init failed");
            ByteBuffer buffer = ByteBuffer.allocateDirect(16384);
            while (!closed) {
                buffer.clear();
                if (!request.queue(buffer)) throw new IOException("USB request queue failed");
                UsbRequest result = connection.requestWait();
                if (closed) break;
                if (result == null) throw new IOException("USB receive failed");
                int count = buffer.position();
                if (count == 0) continue;
                byte[] bytes = new byte[count];
                buffer.flip(); buffer.get(bytes);
                if (!incoming.offer(bytes)) throw new IOException("Android USB receive queue overflow");
            }
        } catch (Exception error) {
            if (!closed) readFailure = new IOException("USB reader: " + error, error);
        } finally { request.cancel(); request.close(); }
    }

    public synchronized byte[] read(int size) throws IOException {
        if (closed) throw new IOException("USB stream closed");
        if (readFailure != null) throw readFailure;
        try {
            byte[] bytes = remainder.length > 0 ? remainder : incoming.poll(20, TimeUnit.MILLISECONDS);
            if (bytes == null) return new byte[0];
            int count = Math.min(size, bytes.length);
            remainder = Arrays.copyOfRange(bytes, count, bytes.length);
            return Arrays.copyOf(bytes, count);
        } catch (InterruptedException error) {
            Thread.currentThread().interrupt();
            throw new IOException(error);
        }
    }

    /** Bytes received and not yet read. */
    public synchronized int available() {
        int count = remainder.length;
        for (byte[] chunk : incoming) count += chunk.length;
        return count;
    }

    /** CDC SET_CONTROL_LINE_STATE: bit 0 DTR, bit 1 RTS. The native USB peripheral resets the chip on
     *  the sequence esptool sends (ESP-IDF, USB Serial/JTAG controller). A CP210x takes CP210X_SET_MHS with
     *  the same two bits and their write masks (bits 8 and 9); a classic ESP32 board wires DTR and RTS to
     *  GPIO0 and EN through its auto-reset transistors, so both on (or both off) keeps it running. */
    public void setLines(boolean dtr, boolean rts) throws IOException {
        int value = (dtr ? 1 : 0) | (rts ? 2 : 0);
        if (cp210x) {
            vendor(SET_MHS, value | 0x0300, null, "CP210x line state");
            return;
        }
        if (connection.controlTransfer(0x21, 0x22, value, control.getId(), null, 0, 1000) < 0)
            throw new IOException("CDC line state failed");
    }

    public void setBaud(int baud) throws IOException {
        byte[] rate = {(byte)baud, (byte)(baud >> 8), (byte)(baud >> 16), (byte)(baud >> 24)};
        if (cp210x) {
            vendor(SET_BAUDRATE, 0, rate, "CP210x baud rate");
            return;
        }
        byte[] coding = {rate[0], rate[1], rate[2], rate[3], 0, 0, 8};
        if (connection.controlTransfer(0x21, 0x20, 0, control.getId(), coding, 7, 1000) != 7)
            throw new IOException("CDC line coding failed");
    }

    private void vendor(int request, int value, byte[] payload, String what) throws IOException {
        int length = payload == null ? 0 : payload.length;
        if (connection.controlTransfer(CP210X_OUT, request, value, data.getId(), payload, length, 1000) < length)
            throw new IOException(what + " failed");
    }

    public boolean isClosed() { return closed || readFailure != null || writeFailure != null; }

    public int write(byte[] bytes) throws IOException {
        if (!queuedWrites) return writeNow(bytes);
        if (closed) throw new IOException("USB stream closed");
        if (writeFailure != null) throw writeFailure;
        synchronized (writeProgress) {
            if (!outgoing.offer(bytes)) throw new IOException("USB write queue overflow");
            enqueuedBytes += bytes.length;
        }
        return bytes.length;
    }

    public void setQueuedWrites(boolean enabled) throws IOException {
        if (!flushWrites(10000)) throw new IOException("USB write flush timeout");
        queuedWrites = enabled;
    }

    public boolean flushWrites(long timeoutMs) throws IOException {
        long deadline = System.nanoTime() + timeoutMs * 1000000;
        synchronized (writeProgress) {
            long target = enqueuedBytes;
            while (sentBytes < target) {
                if (writeFailure != null) throw writeFailure;
                long left = deadline - System.nanoTime();
                if (left <= 0) return false;
                try { TimeUnit.NANOSECONDS.timedWait(writeProgress, left); }
                catch (InterruptedException error) { Thread.currentThread().interrupt(); throw new IOException(error); }
            }
        }
        return true;
    }

    private void writeLoop() {
        try {
            while (!closed) {
                byte[] first = outgoing.take();
                ByteArrayOutputStream batch = new ByteArrayOutputStream(4096);
                batch.write(first, 0, first.length);
                long deadline = System.nanoTime() + 1000000;
                while (batch.size() < 4096) {
                    long left = deadline - System.nanoTime();
                    byte[] next = outgoing.poll(Math.max(0, left), TimeUnit.NANOSECONDS);
                    if (next == null) break;
                    batch.write(next, 0, next.length);
                }
                byte[] bytes = batch.toByteArray();
                writeNow(bytes);
                synchronized (writeProgress) {
                    sentBytes += bytes.length;
                    writeProgress.notifyAll();
                }
            }
        } catch (Exception error) {
            if (!closed) writeFailure = new IOException("USB writer: " + error, error);
            synchronized (writeProgress) { writeProgress.notifyAll(); }
        }
    }

    private int writeNow(byte[] bytes) throws IOException {
        if (closed) throw new IOException("USB stream closed");
        int at = 0;
        while (at < bytes.length) {
            int count = connection.bulkTransfer(output, bytes, at, bytes.length - at, 1000);
            if (count <= 0) throw new IOException("USB write failed at " + at);
            at += count;
        }
        return at;
    }

    @Override public synchronized void close() {
        if (closed) return;
        closed = true;
        if (writer != null) writer.interrupt();
        if (cp210x) {
            connection.controlTransfer(CP210X_OUT, IFC_ENABLE, 0, data.getId(), null, 0, 1000);
            connection.releaseInterface(data);
        } else {
            connection.releaseInterface(data);
            connection.releaseInterface(control);
        }
        connection.close();
    }
}
