"""Spanish for the screens gui/i18n.py's ES does not cover: the Pokemon form, gifts, saves, the Board and Docs
pages, the board status lines (gui/app.py), and the FireRed/LeafGreen catalogue and gift presets the app shows
(pokeldn.app.catalog, pokeldn.app.command, pokeldn.app.gift_builder, pokeldn.frlg.gift.builder). Same rule as
ES: the English text is the key; gui/i18n.py merges this dict into ES."""

ES_EXTRA = {
    # widgets and docs
    "Loading": "Cargando",
    "Copy code": "Copiar código",
    "Browse": "Examinar",
    "Open the docs website": "Abrir el sitio de la guía",
    "Start here": "Empieza aquí",
    "Documentation": "Documentación",

    # the Pokemon form (gui/views/pokemon.py)
    "Build": "Generar",
    "Loading species...": "Cargando especies...",
    "Loading species": "Cargando especies",
    "Nickname (optional)": "Mote (opcional)",
    "Species": "Especie",
    "Level": "Nivel",
    "Shiny": "Shiny",
    "Or use a Pokemon file": "O usa un archivo de Pokémon",
    "Import paste": "Importar texto",
    "or drop either here": "o suelta cualquiera aquí",
    "Unavailable": "No disponible",
    "Search a species": "Busca una especie",
    "Pick a species first.": "Primero elige una especie.",
    "Finding a legal encounter...": "Buscando un encuentro legal...",
    "{n} files dropped; the first was used.": "Soltaste {n} archivos; se usó el primero.",
    "Could not read {name}: {error}": "No se pudo leer {name}: {error}",
    "Not a Pokemon this game can take: {error}": "No es un Pokémon que este juego acepte: {error}",
    "Apply": "Aplicar",
    "Paste a set first.": "Primero pega un set.",
    "Reading the set": "Leyendo el set",
    "Reading the set...": "Leyendo el set...",
    "Set {n}": "Set {n}",
    "The paste holds {n} Pokemon; the first was imported.": "El texto tiene {n} Pokémon; se importó el primero.",
    "Import a Showdown set": "Importar un set de Showdown",
    "Paste a set exported from Pokemon Showdown, Smogon or PKHeX. Its values fill the form; press Build to make "
    "a legal Pokemon from them.":
        "Pega un set exportado de Pokémon Showdown, Smogon o PKHeX. Sus valores llenan el formulario; presiona "
        "Generar para crear con ellos un Pokémon legal.",
    "Imported {name}. Check the options below, then press Build.":
        "Se importó {name}. Revisa las opciones de abajo y presiona Generar.",
    "Building Pokemon": "Generando Pokémon",
    "Legal": "Legal",
    "Not legal": "No legal",
    "Add a trade": "Agregar un intercambio",
    "Remove this trade": "Quitar este intercambio",
    "Trade {n}": "Intercambio {n}",
    "{n} of {limit}, traded in this order": "{n} de {limit}, se intercambian en este orden",
    "Up to {limit} Pokemon in one session": "Hasta {limit} Pokémon en una sesión",
    "; or drop files here": "; o suelta archivos aquí",
    "{n} did not fit: one session trades at most {limit}.":
        "{n} no cupieron: una sesión intercambia {limit} como máximo.",
    "The paste holds {n} Pokemon; the others went to trade {numbers}.":
        "El texto tiene {n} Pokémon; los demás fueron al intercambio {numbers}.",
    "The paste holds {n} Pokemon; the others went to trades {numbers}.":
        "El texto tiene {n} Pokémon; los demás fueron a los intercambios {numbers}.",
    "The paste holds {n} Pokemon; only the first fit.": "El texto tiene {n} Pokémon; solo cupo el primero.",
    "More options": "Más opciones",
    "{n} set": "{n} elegidas",
    "random": "al azar",
    "Loading options": "Cargando opciones",
    "Reading what this species can have...": "Viendo qué puede tener esta especie...",
    "Nature": "Naturaleza",
    "Form": "Forma",
    "Ability": "Habilidad",
    "Ball": "Poké Ball",
    "Held item": "Objeto equipado",
    "Male": "Macho",
    "Female": "Hembra",
    ", {total} in all": ", {total} en total",
    "Effort levels": "Niveles de esfuerzo",
    "HP": "PS",
    "Atk": "Atq",
    "SpA": "AtqEsp",
    "SpD": "DefEsp",
    "Spe": "Vel",
    "Empty means random. The build is checked by PKHeX's legality analysis.":
        "Vacío es al azar. El análisis de legalidad de PKHeX revisa el resultado.",
    "Clear": "Limpiar",
    "Random": "Al azar",
    "Any": "Cualquiera",
    "Moves (empty means the encounter's own)": "Movimientos (vacío: los del encuentro)",
    "EVs add up to at most {total}.": "Los EVs suman {total} como máximo.",
    "Loading...": "Cargando...",
    "Loading names": "Cargando nombres",
    "Not set": "Sin elegir",
    "Search": "Buscar",
    "Slot {n}": "Casilla {n}",

    # the gift builder (gui/views/gifts.py)
    "Use a preset": "Regalos listos",
    "Official events": "Eventos oficiales",
    "Build your own": "Crea el tuyo",
    "Open a file": "Abrir un archivo",
    "Your save": "Tu partida",
    "Save gift file": "Guardar archivo de regalo",
    "Customize": "Personalizar",
    "Before you send": "Antes de enviar",
    "Has settings": "Tiene ajustes",
    "These boosts are always saved in your game.": "Estas mejoras siempre se guardan en tu partida.",
    "Room on the console": "Espacio en la consola",
    "{used} of {room} bytes": "{used} de {room} bytes",
    "The selected boosts run together. Sending a new selection replaces the boosts already running.":
        "Las mejoras elegidas funcionan juntas. Enviar una nueva selección reemplaza las que ya están activas.",
    "Search: Pikachu, Master Ball, shiny...": "Buscar: Pikachu, Master Ball, shiny...",
    "{n} of {total} cards": "{n} de {total} tarjetas",
    "All": "Todos",
    "Real event cards from the projectpokemon EventsGallery archive. Each one passed the game's own card check.":
        "Tarjetas de eventos reales del archivo EventsGallery de projectpokemon. Todas pasaron la revisión de "
        "tarjetas del propio juego.",
    "A .pokegift someone shared, or a {kind} Wonder Card.":
        "Un .pokegift que alguien compartió, o una Tarjeta Misteriosa {kind}.",
    "Card icon": "Icono de la tarjeta",
    "Leave empty to keep the file's own icon.": "Déjalo vacío para conservar el icono del archivo.",
    "Move {n}": "Movimiento {n}",
    "Line {n}": "Línea {n}",
    "Title": "Título",
    "Subtitle": "Subtítulo",
    "Text on the card": "Texto de la tarjeta",
    "Icon": "Icono",
    "Card id": "ID de la tarjeta",
    "Can be received again": "Se puede recibir otra vez",
    "Otherwise once per save.": "Si no, una vez por partida.",
    "The player can share it": "El jugador puede compartirla",
    "Mystery Gift, Wonder Cards, Send.": "Desde Mystery Gift, Wonder Cards, Send.",
    "The card": "La tarjeta",
    "Who hands it over": "Quién la entrega",
    "What happens": "Qué pasa",
    "Item": "Objeto",
    "How many": "Cantidad",
    "Message": "Mensaje",
    "{PLAYER} is the player's name. A box holds two lines.":
        "{PLAYER} es el nombre del jugador. Cada cuadro tiene dos líneas.",
    "Earlier": "Antes",
    "Remove": "Quitar",
    "News id": "ID de la noticia",
    "Text, up to ten lines": "Texto, hasta diez líneas",
    "A console keeps news only when it differs from the one it holds; change the id to send the same text again.":
        "La consola solo guarda una noticia si es distinta de la que tiene; cambia el ID para enviar el mismo "
        "texto otra vez.",
    "ARM code runs on the console while it receives, every frame until it returns 1. A fault or a loop hangs the "
    "Mystery Gift menu, so it is run offline first.":
        "El código ARM corre en la consola mientras recibe, en cada fotograma hasta que devuelve 1. Un error o un "
        "bucle congela el menú de Regalo Misterioso, así que primero se prueba sin conexión.",
    "Assembly": "Ensamblador",
    "Or a prebuilt .bin (used instead of the assembly)": "O un .bin ya compilado (se usa en lugar del ensamblador)",
    "Built for": "Hecho para",
    "Any cartridge": "Cualquier cartucho",
    "Expected answer": "Respuesta esperada",
    "any": "cualquiera",
    "Bytes sent back": "Bytes devueltos",
    "Check offline": "Probar sin conexión",
    "Assembled with the GNU Arm toolchain on this computer.":
        "Se ensambla con las herramientas GNU Arm de esta computadora.",
    "Copy": "Copiar",
    "paste this in a terminal, then check again": "pega esto en una terminal y vuelve a revisar",
    "download it from Arm's page, then check again": "descárgalo de la página de Arm y vuelve a revisar",
    "Check again": "Revisar otra vez",
    "Arm's download page": "Página de descargas de Arm",
    "Typing assembly here needs the free GNU Arm assembler. Install it once: {steps}. A prebuilt .bin works "
    "without it.":
        "Para escribir ensamblador aquí necesitas el ensamblador gratuito GNU Arm. Instálalo una vez: {steps}. "
        "Un .bin ya compilado funciona sin él.",
    "Checking…": "Revisando…",
    "Nickname": "Apodo",
    "OT": "EO",
    "The Pokemon arrives shiny.": "El Pokémon llega shiny.",
    "It can Gigantamax; only species with a Gigantamax form.":
        "Puede hacerse Gigamax; solo especies con forma Gigamax.",
    "Add an item": "Agregar un objeto",
    "Official outfits. A card holds six pieces for each gender; the player gets the version for their own.":
        "Atuendos oficiales. Una tarjeta lleva seis prendas para cada género; el jugador recibe la versión del suyo.",
    "Money": "Dinero",
    "Battle Points": "Puntos de Batalla",
    "Starts on the console as soon as it is received.": "Se activa en la consola en cuanto se recibe.",
    "Works on {targets}.": "Funciona en {targets}.",
    "On the console: Mystery Gift, Wonder Cards, Friend, then POKELDN.":
        "En la consola: Mystery Gift, Wonder Cards, Friend y luego POKELDN.",
    "The whole save comes to Your saves, named after the trainer.":
        "La partida completa llega a Tus partidas, con el nombre del entrenador.",
    "The console shows a message and keeps its save as it was.":
        "La consola muestra un mensaje y deja su partida como estaba.",
    "On the console: Mystery Gift, Wonder Cards, Friend, then POKELDN. Back its save up first.":
        "En la consola: Mystery Gift, Wonder Cards, Friend y luego POKELDN. Antes respalda su partida.",
    "{name} replaces the console's save.": "{name} reemplaza la partida de la consola.",
    "The console checks every part, loads it and saves; anything short of that keeps its save.":
        "La consola revisa cada parte, la carga y guarda; si algo falla, conserva su partida.",
    "Then choose CONTINUE on the title screen.": "Luego elige CONTINUE en la pantalla de título.",
    "Export for which cartridge?": "¿Exportar para qué cartucho?",
    "A .wc3 holds one cartridge's gift. Choose its version and language. A .pokegift keeps every supported "
    "cartridge together.":
        "Un .wc3 lleva el regalo de un solo cartucho. Elige su versión e idioma. Un .pokegift reúne todos los "
        "cartuchos compatibles.",
    "Cartridge": "Cartucho",
    "Export": "Exportar",
    "Preparing gift file…": "Preparando el archivo de regalo…",
    "Save Mystery Gift": "Guardar Regalo Misterioso",
    "Saved {path}": "Guardado en {path}",

    # the save library (gui/views/saves.py)
    "Back up from the Switch": "Respaldar desde la Switch",
    "Put a save on the Switch": "Pasar una partida a la Switch",
    "The console sends its whole save to this computer and keeps it as it was. It takes one to four minutes: keep "
    "the Switch near the board until the console shows the message.":
        "La consola envía su partida completa a esta computadora y la deja como estaba. Tarda de uno a cuatro "
        "minutos: mantén la Switch cerca de la placa hasta que la consola muestre el mensaje.",
    "The chosen save goes beside the console's own. The console checks every part of it, loads it and saves. If "
    "anything goes wrong, it keeps the save it had.":
        "La partida elegida se pone junto a la de la consola. La consola revisa cada parte, la carga y guarda. Si "
        "algo sale mal, conserva la partida que tenía.",
    "Neither of its two copies is whole": "Ninguna de sus dos copias está completa",
    "Lv": "Nv.",
    "Add a .sav file": "Agregar un archivo .sav",
    "Open the folder": "Abrir la carpeta",
    "Refresh": "Actualizar",
    "A backup the link cut short goes on from where it stopped.": "Un respaldo que se cortó sigue desde donde se quedó.",
    "Your saves": "Tus partidas",
    "No saves yet. Back one up from the Switch, or add a .sav file":
        "Todavía no hay partidas. Respalda una desde la Switch o agrega un archivo .sav",
    " (drop it here).": " (suéltalo aquí).",
    "More": "Más",
    "Rename": "Renombrar",
    "Export .sav": "Exportar .sav",
    "Delete": "Borrar",
    "View and edit": "Ver y editar",
    "Checking the party with PKHeX...": "Revisando el equipo con PKHeX...",
    "PKHeX could not read the party: {error}": "PKHeX no pudo leer el equipo: {error}",
    "Every Pokemon in the party is legal.": "Todos los Pokémon del equipo son legales.",
    "Restore anyway": "Restaurar de todos modos",
    "PKHeX finds {names} not legal.": "PKHeX marca como no legal: {names}.",
    "Added {name}.": "Se agregó {name}.",
    "Added {name}, but neither of its two copies is whole.":
        "Se agregó {name}, pero ninguna de sus dos copias está completa.",
    "Export save": "Exportar partida",
    "Exported to {path}": "Exportada a {path}",
    "Rename the save": "Renombrar la partida",
    "Delete this save?": "¿Borrar esta partida?",
    "{name} is removed from this computer. The Switch keeps its own save.":
        "{name} se borrará de esta computadora. La Switch conserva su propia partida.",
    "Reading the save with PKHeX...": "Leyendo la partida con PKHeX...",
    "Keep as a new save": "Guardar como partida nueva",
    "Close": "Cerrar",
    "PKHeX could not read this save: {error}": "PKHeX no pudo leer esta partida: {error}",
    "A number": "Un número",
    "ID {tid} · secret ID {sid} · {hours} h {minutes} · {badges} badges · Pokedex {caught} caught, {seen} seen":
        "ID {tid} · ID secreto {sid} · {hours} h {minutes} · {badges} medallas · Pokédex: {caught} capturados, "
        "{seen} vistos",
    "Trainer": "Entrenador",
    "Coins": "Fichas",
    "Add a Pokemon": "Agregar un Pokémon",
    "Party": "Equipo",
    "{n} of {total}": "{n} de {total}",
    "No moves": "Sin movimientos",
    "New Pokemon, for the trainer of this save": "Pokémon nuevo, para el entrenador de esta partida",
    " · egg": " · huevo",
    "Empty": "Vacía",
    "Checking with PKHeX...": "Revisando con PKHeX...",
    "{species} (Lv {level}) is not legal": "{species} (Nv. {level}) no es legal",
    "Every Pokemon in this box is legal.": "Todos los Pokémon de esta caja son legales.",
    "PC boxes": "Cajas del PC",
    "Check legality": "Revisar legalidad",
    "Writing the save...": "Escribiendo la partida...",
    "Kept as {name}. The original is unchanged.": "Guardada como {name}. La original no cambia.",

    # the Board page (gui/views/boards.py)
    "ESP32-S3, C3 or C6 with two USB ports: plug into the one marked USB, not COM or UART.":
        "ESP32-S3, C3 o C6 con dos puertos USB: conéctala al que dice USB, no al COM ni al UART.",
    "Press Flash. The app picks the firmware for your chip and checks the board afterwards.":
        "Presiona Flashear. La app elige el firmware para tu chip y luego revisa la placa.",
    "Stuck on 'Connecting'? Hold the board's BOOT button until writing starts, then let go.":
        "¿Se queda en 'Conectando'? Mantén el botón BOOT de la placa hasta que empiece a escribir y luego suéltalo.",
    "Checks and flashing show their output here.": "Aquí aparece lo que muestran las revisiones y el flasheo.",
    "Boards": "Placas",
    "Scan again": "Buscar otra vez",
    "Activity": "Actividad",
    "In use": "En uso",
    "No board found": "No se encontró ninguna placa",
    "Plug it in with a data cable. It shows up here on its own.": "Conéctala con un cable de datos. Aparece aquí sola.",
    "Checking": "Revisando",
    "Use this board": "Usar esta placa",
    "Go to Games": "Ir a Juegos",
    " Sessions use this board.": " Las sesiones usan esta placa.",
    " Sessions use another board; press Use this board to switch.":
        " Las sesiones usan otra placa; presiona Usar esta placa para cambiar.",
    "not checked yet": "sin revisar todavía",
    "unknown": "desconocida",
    "Living room, spare...": "Sala, repuesto...",
    "Port": "Puerto",
    "USB chip": "Chip USB",
    "Firmware": "Firmware",
    "Wi-Fi MAC": "MAC Wi-Fi",
    "Save the nickname": "Guardar el apodo",
    "Blink the LED": "Hacer parpadear el LED",
    "Details": "Detalles",
    "Blink the LED shows which board this is: a classic ESP32's blue LED blinks for five seconds. A nickname helps "
    "when several are plugged in.":
        "Hacer parpadear el LED te muestra cuál placa es: el LED azul de un ESP32 clásico parpadea cinco segundos. "
        "Un apodo ayuda cuando hay varias conectadas.",
    "Flashing...": "Flasheando...",
    "Flash": "Flashear",
    "Custom image: {path}": "Imagen propia: {path}",
    "Firmware included with the app: ESP32, ESP32-S3, ESP32-C3 or ESP32-C6, picked for your chip.":
        "Firmware incluido con la app: ESP32, ESP32-S3, ESP32-C3 o ESP32-C6, elegido para tu chip.",
    "No firmware image here yet (a copy run from source). Download the released one; no ESP-IDF needed.":
        "Todavía no hay imagen de firmware (copia ejecutada desde el código fuente). Descarga la publicada; no "
        "necesitas ESP-IDF.",
    "Included firmware": "Firmware incluido",
    "Use a firmware file of your own": "Usar un archivo de firmware propio",
    ", or drop a .bin on this card": ", o suelta un .bin en esta tarjeta",
    "Downloading...": "Descargando...",
    "Download the firmware": "Descargar el firmware",
    "Flash the firmware": "Flashear el firmware",
    "Needed once per board, and again after an app update that says so. Takes about thirty seconds.":
        "Hace falta una vez por placa, y otra vez si una actualización de la app lo pide. Tarda unos treinta "
        "segundos.",
    "Connecting...": "Conectando...",
    "Writing {percent}": "Escribiendo {percent}",
    "Done. Checking the board...": "Listo. Revisando la placa...",
    "Flashing failed. Hold the BOOT button and press Flash again; the Activity log has the details.":
        "Falló el flasheo. Mantén el botón BOOT y presiona Flashear otra vez; el registro de Actividad tiene los "
        "detalles.",
    "Try another cable or USB port. Many cables only charge.": "Prueba otro cable u otro puerto USB. Muchos cables solo cargan.",
    "Windows needs the driver for the board's USB chip, printed on the chip next to the USB socket (CP2102 or "
    "CH340):":
        "Windows necesita el driver del chip USB de la placa, impreso en el chip junto al conector USB (CP2102 o "
        "CH340):",
    "CP210x driver": "Driver CP210x",
    "CH340 driver": "Driver CH340",
    "Download the CP210x Universal Windows Driver zip, extract it, right-click silabser.inf and choose Install, "
    "then unplug and replug the board.":
        "Descarga el zip CP210x Universal Windows Driver, descomprímelo, haz clic derecho en silabser.inf y elige "
        "Instalar; luego desconecta y vuelve a conectar la placa.",
    "Download CH341SER.EXE, run it and press Install, then unplug and replug the board.":
        "Descarga CH341SER.EXE, ábrelo y presiona Install; luego desconecta y vuelve a conectar la placa.",
    "Allow serial ports, then log out and back in:": "Permite los puertos serie y luego cierra sesión y vuelve a entrar:",
    "Arch and its derivatives name the group uucp instead of dialout.":
        "Arch y sus derivados llaman al grupo uucp en vez de dialout.",
    "Use a classic ESP32 (ESP32-D0WD, WROOM-32E), or an ESP32-S3, C3 or C6 through its native USB port. S2 boards "
    "are not supported.":
        "Usa un ESP32 clásico (ESP32-D0WD, WROOM-32E), o un ESP32-S3, C3 o C6 por su puerto USB nativo. Las placas "
        "S2 no son compatibles.",
    "Board not listed?": "¿No aparece tu placa?",

    # board status (gui/app.py), shown on Home, the session checklist and the Board page
    "Board found without a serial port": "Placa encontrada sin puerto serie",
    "Ubuntu 22.04's braille service takes CH340 boards: sudo apt remove brltty, then unplug and replug the board.":
        "El servicio de braille de Ubuntu 22.04 se queda con las placas CH340: sudo apt remove brltty, y luego "
        "desconecta y vuelve a conectar la placa.",
    "Unplug and replug it; the kernel log (sudo dmesg) says why.":
        "Desconéctala y vuelve a conectarla; el registro del kernel (sudo dmesg) dice por qué.",
    "Linux gave the {bridge} no serial port. {fix}": "Linux no le dio puerto serie al {bridge}. {fix}",
    "Board found without a driver": "Placa encontrada sin driver",
    "Install its driver; the Board page links it.": "Instala su driver; la página Placa tiene el enlace.",
    "Windows has no driver for the {name}, so it has no COM port. {steps}":
        "Windows no tiene driver para el {name}, así que no tiene puerto COM. {steps}",
    "No board plugged in": "No hay ninguna placa conectada",
    "Plug the ESP32 in with a USB data cable. Charge-only cables show nothing.":
        "Conecta el ESP32 con un cable USB de datos. Los cables que solo cargan no muestran nada.",
    "Several boards plugged in": "Hay varias placas conectadas",
    "Open the Board page and pick the one to use.": "Abre la página Placa y elige cuál usar.",
    "Board unplugged": "Placa desconectada",
    "Plug it back in.": "Vuelve a conectarla.",
    "Board ready": "Placa lista",
    "pokeldn firmware{version} answered.": "El firmware de pokeldn{version} respondió.",
    "Firmware out of date": "Firmware desactualizado",
    "Flash the board to update it.": "Flashea la placa para actualizarla.",
    "Add yourself to the {group} group (sudo usermod -aG {group} $USER), then log out and back in.":
        "Agrégate al grupo {group} (sudo usermod -aG {group} $USER) y luego cierra sesión y vuelve a entrar.",
    "Unplug and replug the board.": "Desconecta y vuelve a conectar la placa.",
    "No permission to open the board": "Sin permiso para abrir la placa",
    "Board port busy": "Puerto de la placa ocupado",
    "Another program holds the port. Close it, or unplug and replug the board.":
        "Otro programa está usando el puerto. Ciérralo, o desconecta y vuelve a conectar la placa.",
    "Use the board's other USB port": "Usa el otro puerto USB de la placa",
    "The {chip} firmware talks over the native USB port. Move the cable to the port marked USB (not COM or UART).":
        "El firmware del {chip} se comunica por el puerto USB nativo. Pasa el cable al puerto que dice USB (no COM "
        "ni UART).",
    "No pokeldn firmware on the board": "La placa no tiene el firmware de pokeldn",
    "Flash the board. If you just flashed it, press its RESET (RST) button.":
        "Flashea la placa. Si acabas de flashearla, presiona su botón RESET (RST).",
    "Checking the board": "Revisando la placa",
    "Asking the board for its firmware.": "Preguntándole a la placa por su firmware.",
    "No pokeldn firmware": "Sin firmware de pokeldn",
    "Port busy or not allowed": "Puerto ocupado o sin permiso",
    "Port not allowed": "Puerto sin permiso",

    # catalog and checks (pokeldn.app.catalog, pokeldn.app.command, pokeldn.app.gift_builder)
    "Pick a species; PKHeX builds a legal one for this game. Add a trade to queue more: one session trades them "
    "in order.":
        "Elige una especie; PKHeX genera uno legal para este juego. Agrega un intercambio para poner más en cola: "
        "una sesión los intercambia en orden.",
    "Build the Pokemon to offer first.": "Primero genera el Pokémon para ofrecer.",
    "The Pokemon is not legal.": "El Pokémon no es legal.",
    "Pick three Pokemon for the link code.": "Elige tres Pokémon para el código de enlace.",
    "Choose the save to put on the console.": "Elige la partida que vas a pasar a la consola.",
    "This save has no whole copy of a game in it.": "Esta partida no tiene ninguna copia completa.",
    "Checking the save's party with PKHeX...": "Revisando el equipo de la partida con PKHeX...",
    "A save backup or restore sends no gift.": "Un respaldo o una restauración de partida no envía ningún regalo.",
    "Open a gift file, or choose a preset.": "Abre un archivo de regalo o elige un regalo listo.",
    "Add at least one step to the gift.": "Agrega al menos un paso al regalo.",
    "Tick at least one boost.": "Marca al menos una mejora.",
    "The Pokemon follower runs alone: untick the other boosts.":
        "El Pokémon acompañante funciona solo: desmarca las otras mejoras.",
    "Shiny countdown and Lead's IVs on screen both draw in the top-right corner: untick one.":
        "Cuenta atrás shiny e IVs del primero en pantalla dibujan en la esquina superior derecha: desmarca una.",
    "Speed up the game: pick a speed above x1 or faster text.":
        "Acelerar el juego: elige una velocidad mayor que x1 o texto más rápido.",

    # FireRed/LeafGreen gift builder (pokeldn.frlg.gift.builder): kinds, givers, steps
    "Wonder Card": "Tarjeta Misteriosa",
    "Wonder News": "Noticias Misteriosas",
    "Console code": "Código de consola",
    "The delivery man": "El repartidor",
    "any Pokemon Center, after the card is saved": "cualquier Centro Pokémon, después de guardar la tarjeta",
    "Mom": "Mamá",
    "the player's house": "la casa del jugador",
    "The man in Pallet Town": "El señor de Pallet Town",
    "south of Pallet Town": "al sur de Pallet Town",
    "Pokemon": "Pokémon",
    "Egg": "Huevo",
    "Wild battle": "Combate salvaje",

    # gift preset groups and intros
    "Wonder Cards": "Tarjetas Misteriosas",
    "Event Pokemon": "Pokémon de evento",
    "10th Anniversary Pokemon": "Pokémon del 10.º aniversario",
    "Change a Pokemon": "Cambiar un Pokémon",
    "Game changes": "Cambios en el juego",
    "More gifts": "Más regalos",
    "Read the save": "Leer la partida",
    "Game boosts": "Mejoras del juego",
    "A game boost is a change to how your game plays, such as walking through walls or a faster game. Select the "
    "boosts and send them through Mystery Gift. They start immediately and stop when you restart the game or turn "
    "off the console. To restore them later, save them in the game and send Mom's gift below.":
        "Una mejora del juego cambia cómo se juega, como atravesar paredes o un juego más rápido. Elige las mejoras "
        "y envíalas por Regalo Misterioso. Se activan al instante y se detienen cuando reinicias el juego o apagas "
        "la consola. Para recuperarlas después, guárdalas en la partida y envía el regalo de Mamá de abajo.",
    "Read your Trainer ID (TID), Secret ID (SID), or your party's stats in the Session log. The TID appears on your "
    "Trainer Card; the SID is normally hidden. IVs are a Pokemon's six individual stat values, from 0 to 31. EVs "
    "are stat points gained through training. These tools keep your save and Wonder Card unchanged.":
        "Lee tu ID de entrenador (TID), tu ID secreto (SID) o las estadísticas de tu equipo en el registro de la "
        "sesión. El TID aparece en tu tarjeta de entrenador; el SID normalmente está oculto. Los IVs son los seis "
        "valores individuales de un Pokémon, de 0 a 31. Los EVs son puntos de estadística que se ganan entrenando. "
        "Estas herramientas no cambian tu partida ni tu Tarjeta Misteriosa.",

    # when to use a preset, shown before sending
    "After the card is saved, talk to the delivery man on 2F of any Pokemon Center.":
        "Después de guardar la tarjeta, habla con el repartidor en el 2.º piso de cualquier Centro Pokémon.",
    "Receive it through Mystery Gift, then read the results in the Session log. Your save and Wonder Card are kept.":
        "Recíbelo por Regalo Misterioso y lee los resultados en el registro de la sesión. Tu partida y tu Tarjeta "
        "Misteriosa se conservan.",
    "First send boosts saved in your game, using Save boosts for later when available. Then send this gift. After "
    "each restart, talk to Mom at home in Pallet Town to turn the boosts back on. Send this gift again if you "
    "receive another Wonder Card.":
        "Primero envía mejoras guardadas en tu partida, con Guardar mejoras para después cuando esté disponible. "
        "Luego envía este regalo. Después de cada reinicio, habla con Mamá en tu casa de Pallet Town para volver a "
        "activarlas. Envía este regalo otra vez si recibes otra Tarjeta Misteriosa.",

    # Wonder Card presets
    "Legendary beast": "Bestia legendaria",
    "Two berries, a Master Ball and a battle with the beast that follows the starter.":
        "Dos bayas, una Master Ball y un combate con la bestia que corresponde a tu inicial.",
    "A level 50 Celebi from the delivery man.": "Un Celebi de nivel 50 del repartidor.",
    "One Master Ball.": "Una Master Ball.",
    "Changes which Pokemon live in Altering Cave.": "Cambia qué Pokémon viven en Altering Cave.",
    "Wish Egg": "Huevo con Wish",
    "One of six eggs that knows Wish, picked by the console.": "Uno de seis huevos que saben Wish, elegido por la consola.",
    "PokePark egg": "Huevo de PokePark",
    "One of fifteen eggs with special moves, picked by the console.":
        "Uno de quince huevos con movimientos especiales, elegido por la consola.",
    "Pokemon Center Japan egg": "Huevo del Pokémon Center de Japón",
    "One of four eggs with special moves.": "Uno de cuatro huevos con movimientos especiales.",
    "Starter egg": "Huevo de inicial",
    "An egg of one of the nine first partners.": "Un huevo de uno de los nueve Pokémon iniciales.",
    "Rare berries": "Bayas raras",
    "An Enigma, a Lansat and a Starf Berry.": "Una Enigma Berry, una Lansat Berry y una Starf Berry.",
    "National Pokedex": "Pokédex Nacional",
    "Upgrades the Pokedex to the National Pokedex.": "Mejora la Pokédex a la Pokédex Nacional.",
    "Porygon TM gift": "Porygon y MT de regalo",
    "A Porygon and a TM.": "Un Porygon y una MT.",
    "Sun and Moon Rally: Solrock": "Rally Sol y Luna: Solrock",
    "Sun and Moon Rally: Lunatone": "Rally Sol y Luna: Lunatone",
    "A rally stamp.": "Un sello del rally.",
    "Visiting trainer": "Entrenador visitante",
    "A trainer who waits in the Pokemon Center.": "Un entrenador que espera en el Centro Pokémon.",
    "Battle count card": "Tarjeta contador de combates",
    "A card that counts link battles.": "Una tarjeta que cuenta los combates por cable.",
    "The Worlds card.": "La tarjeta de Worlds.",

    # GB-Link Team presets: change a Pokemon
    "Nature mint": "Menta de naturaleza",
    "Pick which stat a Pokemon's nature raises and lowers.":
        "Elige qué estadística sube y baja la naturaleza de un Pokémon.",
    "Ability capsule": "Cápsula de habilidad",
    "Switches a Pokemon to its other ability.": "Cambia un Pokémon a su otra habilidad.",
    "Poke Ball changer": "Cambio de Poké Ball",
    "Moves a Pokemon into the ball you choose.": "Pasa un Pokémon a la Poké Ball que elijas.",
    "Gender change": "Cambio de sexo",
    "Switches a Pokemon between male and female.": "Cambia un Pokémon entre macho y hembra.",
    "Nickname change": "Cambio de mote",
    "A new nickname, or the species name back.": "Un mote nuevo, o vuelve al nombre de la especie.",
    "IV and EV judge": "Juez de IVs y EVs",
    "Shows a Pokemon's nature, six IVs and EVs on screen.":
        "Muestra en pantalla la naturaleza, los seis IVs y los EVs de un Pokémon.",
    "Hidden Power and max IVs": "Hidden Power e IVs al máximo",
    "Shows its Hidden Power, then can set every IV to 31.": "Muestra su Hidden Power y puede poner todos los IVs en 31.",
    "Hidden Power type": "Tipo de Hidden Power",
    "Gives Hidden Power the type you pick.": "Le da a Hidden Power el tipo que elijas.",
    "EV training": "Entrenamiento de EVs",
    "Resets EVs or maxes the stats you pick, no battles.":
        "Reinicia los EVs o maximiza las estadísticas que elijas, sin combates.",
    "Friendship checker": "Medidor de amistad",
    "Shows friendship and can max it.": "Muestra la amistad y puede llevarla al máximo.",
    "Every move in the party gets its most PP.": "Cada movimiento del equipo recibe sus PP máximos.",
    "Max conditions": "Condiciones al máximo",
    "Contest stats to the max; Feebas then evolves.": "Estadísticas de concurso al máximo; así Feebas evoluciona.",
    "Pokerus": "Pokérus",
    "The party catches Pokerus, which doubles EVs earned.":
        "El equipo se contagia de Pokérus, que duplica los EVs ganados.",
    "Unown letter": "Letra de Unown",
    "Gives an Unown any letter.": "Le da a un Unown cualquier letra.",
    "Trade evolution": "Evolución por intercambio",
    "Evolves a trade-evolution Pokemon, no trade.":
        "Evoluciona a un Pokémon que evoluciona por intercambio, sin intercambiar.",
    "Espeon or Umbreon": "Espeon o Umbreon",
    "A friendly Eevee evolves into the one you pick.": "Un Eevee con mucha amistad evoluciona en el que elijas.",
    "Move relearner and deleter": "Recordar y olvidar movimientos",
    "Relearn or forget a move; the move tutors teach again.":
        "Recuerda u olvida un movimiento; los tutores de movimientos vuelven a enseñar.",

    # GB-Link Team presets: game changes (most add STOPS below)
    "Double speed": "Velocidad doble",
    "Triple speed": "Velocidad triple",
    "Quadruple speed": "Velocidad cuádruple",
    "Slower game": "Juego más lento",
    "Half speed": "Media velocidad",
    "Fast text": "Texto rápido",
    "Fly with R": "Volar con R",
    "PC anywhere": "PC en cualquier lugar",
    "HM moves without HMs": "Movimientos MO sin MO",
    "Reusable TMs": "MT reutilizables",
    "Physical/special split": "División física/especial",
    "Exp. Share for all": "Exp. Share para todos",
    "Shiny chain": "Cadena shiny",
    "Roaming Pokemon finder": "Buscador de Pokémon errantes",
    "No encounters or repel": "Sin encuentros o repelente",
    "No wild Pokemon, or only stronger ones, until the game is reset.":
        "Sin Pokémon salvajes, o solo los más fuertes, hasta que reinicies el juego.",
    "Legendary respawn": "Legendarios de vuelta",
    "Legendaries you beat without catching come back.": "Los legendarios que derrotaste sin atrapar vuelven a aparecer.",
    "Instant eggs": "Huevos al instante",
    "Hatches the eggs you carry, or readies the Day Care egg.":
        "Eclosiona los huevos que llevas o deja listo el huevo de la Guardería.",

    # GB-Link Team presets: more gifts
    "Gift box": "Caja de regalos",
    "100,000 money, 99 Rare Candies and 1,000 coins.": "100,000 de dinero, 99 Rare Candies y 1,000 fichas.",
    "Pocket casino": "Casino de bolsillo",
    "Play the slot machines from the delivery man.": "Juega a las tragamonedas con el repartidor.",
    "Gift ribbons": "Cintas de regalo",
    "The party gets the seven event ribbons.": "El equipo recibe las siete cintas de evento.",
    "Trainer ID and Secret ID on screen": "ID de entrenador e ID secreto en pantalla",
    "The delivery man tells your Trainer ID and Secret ID.": "El repartidor te dice tu ID de entrenador y tu ID secreto.",
    "New trainer name or look": "Nuevo nombre o aspecto del entrenador",
    "Rename yourself, or switch between boy and girl.": "Cámbiate el nombre, o cambia entre chico y chica.",
    "Rename your rival": "Renombrar a tu rival",
    "Gives your rival a new name.": "Le da un nombre nuevo a tu rival.",

    # event Pokemon (their names stay as the games print them)
    "The Colosseum Bonus Disc Jirachi, level 5.": "El Jirachi del disco extra de Colosseum, nivel 5.",
    "The Pokemon Channel Jirachi, level 5.": "El Jirachi de Pokémon Channel, nivel 5.",
    "The Aura Mew, level 10.": "El Aura Mew, nivel 10.",
    "The MYSTRY Mew, level 10.": "El MYSTRY Mew, nivel 10.",
    "The DOEL Deoxys, level 70.": "El DOEL Deoxys, nivel 70.",
    "The SPACE C Deoxys, level 70.": "El SPACE C Deoxys, nivel 70.",
    "The ROCKS Metang, level 30, with the National Ribbon.": "El ROCKS Metang, nivel 30, con la National Ribbon.",
    "Level 70, from the 10th anniversary.": "Nivel 70, del 10.º aniversario.",
    "Pokemon Box eggs": "Huevos de Pokémon Box",
    "A Swablu, Zigzagoon, Skitty or Pichu egg with a special move.":
        "Un huevo de Swablu, Zigzagoon, Skitty o Pichu con un movimiento especial.",
    "Colosseum Pikachu": "Pikachu de Colosseum",
    "The Japanese Colosseum bonus disc Pikachu. Its Japanese trainer name shows as dots.":
        "El Pikachu del disco extra japonés de Colosseum. Su nombre de entrenador japonés se ve como puntos.",
    "The Japanese Colosseum bonus disc Celebi. Its Japanese trainer name shows as dots.":
        "El Celebi del disco extra japonés de Colosseum. Su nombre de entrenador japonés se ve como puntos.",
    "The Ho-Oh Colosseum gave for 100 Mt. Battle wins.": "El Ho-Oh que Colosseum daba por 100 victorias en Mt. Battle.",

    # Wonder News presets
    "One berry in Cerulean City": "Una baya en Cerulean City",
    "A short news; the man in Cerulean City hands over a berry.":
        "Una noticia corta; el señor de Cerulean City te da una baya.",
    "Ten-line news": "Noticia de diez líneas",
    "A long news that scrolls, with a berry.": "Una noticia larga que se desplaza, con una baya.",

    # game boosts
    "Select boosts to run together. Save them for Mom to restore after a restart.":
        "Elige mejoras para usarlas juntas. Guárdalas para que Mamá las restaure después de reiniciar.",
    "Mom restores your boosts": "Mamá restaura tus mejoras",
    "Send after saving your boosts. Talk to Mom in Pallet Town to restore them after each restart. Another Wonder "
    "Card replaces this gift.":
        "Envíalo después de guardar tus mejoras. Habla con Mamá en Pallet Town para restaurarlas después de cada "
        "reinicio. Otra Tarjeta Misteriosa reemplaza este regalo.",
    "Save boosts for later": "Guardar mejoras para después",
    "Speed up the game": "Acelerar el juego",
    "x2, x3 or x4 in the overworld and in battle, and faster text.":
        "x2, x3 o x4 en el mundo y en los combates, y texto más rápido.",
    "Walk through walls": "Atravesar paredes",
    "Hold a button to walk through walls, trees and water.": "Mantén un botón para atravesar paredes, árboles y agua.",
    "No wild encounters": "Sin encuentros salvajes",
    "No grass, water or roaming encounters.": "Sin encuentros en la hierba, en el agua ni con errantes.",
    "Shiny countdown": "Cuenta atrás shiny",
    "Counts down to the next shiny in the grass.": "Cuenta cuánto falta para el próximo shiny en la hierba.",
    "Lead's IVs on screen": "IVs del primero en pantalla",
    "The lead Pokemon's IVs and nature, top right.": "Los IVs y la naturaleza del primer Pokémon, arriba a la derecha.",
    "Pokemon follower": "Pokémon acompañante",
    "Your lead Pokemon walks behind you.": "Tu primer Pokémon camina detrás de ti.",
    "Game speed": "Velocidad del juego",
    "Where": "Dónde",
    "When": "Cuándo",
    "Faster text": "Texto más rápido",
    "Dialogue prints several letters a frame.": "Los diálogos muestran varias letras por fotograma.",
    "Slow the game down": "Hacer el juego más lento",
    "By": "Cuánto",
    "Always on": "Siempre activo",
    "Hold R": "Mantener R",
    "Hold B (also runs)": "Mantener B (también corre)",
    "Hold Select (also uses the registered item)": "Mantener Select (también usa el objeto registrado)",
    "Overworld and battles": "Mundo y combates",
    "Overworld only": "Solo el mundo",
    "Battles only": "Solo combates",
    "x2 slower": "x2 más lento",
    "x4 slower": "x4 más lento",
    "x8 slower": "x8 más lento",
    "Text prints faster": "El texto sale más rápido",
    "Counts down to the next shiny wild Pokemon in the grass, top right of the screen":
        "Cuenta cuánto falta para el próximo Pokémon salvaje shiny en la hierba, arriba a la derecha de la pantalla",
    "No grass, water or roaming encounters; fishing and Sweet Scent still work":
        "Sin encuentros en la hierba, en el agua ni con errantes; pescar y Sweet Scent siguen funcionando",
    "The lead Pokemon's six IVs and its nature, top right of the overworld":
        "Los seis IVs y la naturaleza del primer Pokémon, arriba a la derecha en el mundo",
    "The lead Pokemon walks behind you, hops ledges with you, and smiles and cries when you face it and press A":
        "El primer Pokémon camina detrás de ti, salta los bordes contigo, y sonríe y hace su grito cuando lo miras "
        "y presionas A",
    "These boosts stop when you restart the game or turn off the console.":
        "Estas mejoras se detienen cuando reinicias el juego o apagas la consola.",

    # Trainer ID and save readouts
    "Trainer ID (TID) and Secret ID (SID)": "ID de entrenador (TID) e ID secreto (SID)",
    "Shows both IDs in the Session log: your Trainer Card's ID and the normally hidden Secret ID.":
        "Muestra ambos ID en el registro de la sesión: el de tu tarjeta de entrenador y el ID secreto, que "
        "normalmente está oculto.",
    "Trainer name, IDs and play time": "Nombre, ID y tiempo de juego",
    "Shows your name, Trainer ID (TID), Secret ID (SID) and play time in the Session log. Saves a copy of the read "
    "data in Received.":
        "Muestra tu nombre, tu ID de entrenador (TID), tu ID secreto (SID) y el tiempo de juego en el registro de la "
        "sesión. Guarda una copia de los datos leídos en Recibidos.",
    "Your party's IVs and natures": "IVs y naturalezas de tu equipo",
    "Shows each Pokemon in your last saved party: nature, six IVs (0-31) and EVs in the Session log. Saves a copy "
    "of the read data in Received.":
        "Muestra cada Pokémon de tu último equipo guardado: naturaleza, seis IVs (0-31) y EVs en el registro de la "
        "sesión. Guarda una copia de los datos leídos en Recibidos.",

    # what a built card does (describe())
    "Shown on the Wonder News screen as soon as it is received.":
        "Aparece en la pantalla de Wonder News en cuanto se recibe.",
    "Runs on the console while it receives, inside the Mystery Gift menu.":
        "Se ejecuta en la consola mientras recibe, dentro del menú Mystery Gift.",
    "Your ARM code, checked offline before it is sent": "Tu código ARM, probado sin conexión antes de enviarlo",
    "Built for any cartridge; call no ROM address": "Hecho para cualquier cartucho; no llames ninguna dirección de la ROM",
    "Runs when the player talks to the delivery man, any Pokemon Center, after the card is saved.":
        "Se activa cuando el jugador habla con el repartidor, en cualquier Centro Pokémon, después de guardar la "
        "tarjeta.",
    "Runs when the player talks to mom in the player's house. The card is not shown while that person holds the "
    "gift.":
        "Se activa cuando el jugador habla con Mamá en la casa del jugador. La tarjeta no se muestra mientras esa "
        "persona tenga el regalo.",
    "Runs when the player talks to the man in pallet town in south of Pallet Town. The card is not shown while "
    "that person holds the gift.":
        "Se activa cuando el jugador habla con el señor de Pallet Town, al sur de Pallet Town. La tarjeta no se "
        "muestra mientras esa persona tenga el regalo.",
    "Every time the player talks to mom, until another gift is received":
        "Cada vez que el jugador hable con Mamá, hasta que reciba otro regalo",
    "Every time the player talks to the man in pallet town, until another gift is received":
        "Cada vez que el jugador hable con el señor de Pallet Town, hasta que reciba otro regalo",
    "Received once per save": "Se recibe una vez por partida",
    "The player can pass the card on": "El jugador puede pasar la tarjeta a otros",
}


# Templates the code fills before translating: one key per value it can take.

# command.missing_offer, for a queue of up to six trades
for _n in range(1, 7):
    ES_EXTRA[f"Build the Pokemon to offer for trade {_n} first."] = (
        f"Primero genera el Pokémon para ofrecer en el intercambio {_n}.")
    ES_EXTRA[f"The Pokemon for trade {_n} is not legal."] = f"El Pokémon del intercambio {_n} no es legal."

# Cartridges, as pokeldn.frlg.gift.builder.CARTRIDGES names them, and the code card built for one
_VERSIONS = {"FireRed": "Rojo Fuego", "LeafGreen": "Verde Hoja"}
_LANGUAGES = {"English": "inglés", "French": "francés", "German": "alemán", "Italian": "italiano",
              "Spanish": "español", "Japanese": "japonés"}
for _version, _version_es in _VERSIONS.items():
    for _language, _language_es in _LANGUAGES.items():
        ES_EXTRA[f"{_version} ({_language})"] = f"{_version_es} ({_language_es})"
        ES_EXTRA[f"Built for {_version} ({_language})"] = f"Hecho para {_version_es} ({_language_es})"

# Game changes that stop the resident boosts (builder.STOPS_BOOSTS)
_STOPS = (" Turns off any game boost that is on.", " Apaga cualquier mejora del juego que esté activa.")
for _en, _es in (
        ("R turns double speed on and off.", "R activa y desactiva la velocidad doble."),
        ("R turns triple speed on and off.", "R activa y desactiva la velocidad triple."),
        ("R turns x4 speed on and off.", "R activa y desactiva la velocidad x4."),
        ("R plays a little slower.", "Con R el juego va un poco más lento."),
        ("R plays at half speed.", "Con R el juego va a media velocidad."),
        ("All text prints at once until the game is reset.",
         "Todo el texto aparece de golpe hasta que reinicies el juego."),
        ("R flies from outdoors, no HM; run and bike anywhere.",
         "R vuela desde exteriores, sin MO; corre y usa la bici en cualquier lugar."),
        ("R opens the Pokemon boxes from anywhere.", "R abre las cajas Pokémon desde cualquier lugar."),
        ("Cut, Surf, Strength and more with only the badge.", "Cut, Surf, Strength y más solo con la medalla."),
        ("Teaching a TM no longer uses it up.", "Enseñar una MT ya no la gasta."),
        ("Each move is physical or special as in later games.",
         "Cada movimiento es físico o especial, como en juegos posteriores."),
        ("The whole party gets Exp. from every battle.", "Todo el equipo gana Exp. en cada combate."),
        ("Meeting one species again and again makes it shiny more often; R shows the chain.",
         "Encontrar la misma especie una y otra vez la hace shiny más seguido; R muestra la cadena."),
        ("Says where the roaming Pokemon is and can lure it.", "Dice dónde está el Pokémon errante y puede atraerlo.")):
    ES_EXTRA[_en + _STOPS[0]] = _es + _STOPS[1]

# Mom's steps (builder.MOM_STEPS) and the texts built on them
_MOM_STEPS = ('After sending the saved boosts, send "Mom restores your boosts" once. After each restart, talk to '
              "Mom at home in Pallet Town to turn them back on. Send Mom's gift again if you receive another "
              "Wonder Card.",
              'Después de enviar las mejoras guardadas, envía "Mamá restaura tus mejoras" una vez. Después de cada '
              "reinicio, habla con Mamá en tu casa de Pallet Town para volver a activarlas. Envía otra vez el "
              "regalo de Mamá si recibes otra Tarjeta Misteriosa.")
ES_EXTRA[_MOM_STEPS[0]] = _MOM_STEPS[1]
ES_EXTRA["Keep a copy of these boosts in your save. " + _MOM_STEPS[0]] = (
    "Guarda una copia de estas mejoras en tu partida. " + _MOM_STEPS[1])
ES_EXTRA["These boosts are saved in your game. " + _MOM_STEPS[0]] = (
    "Estas mejoras se guardan en tu partida. " + _MOM_STEPS[1])

# What the ticked boosts do (builder._turbo, _shiny, _noclip)
_BUTTONS = ("R", "B", "Select")
_WHERE = {"Overworld and battles": "Mundo y combates", "Overworld only": "Solo el mundo",
          "Battles only": "Solo combates"}
_SLOWER = {"x2 slower": "x2 más lento", "x4 slower": "x4 más lento", "x8 slower": "x8 más lento"}
for _where, _where_es in _WHERE.items():
    for _speed in (2, 3, 4):
        ES_EXTRA[f"{_where} run up to x{_speed} all the time"] = f"{_where_es}: hasta x{_speed} todo el tiempo"
        for _button in _BUTTONS:
            ES_EXTRA[f"{_where} run up to x{_speed} while {_button} is held"] = (
                f"{_where_es}: hasta x{_speed} mientras mantienes {_button}")
for _button in _BUTTONS:
    ES_EXTRA[f"Walk through walls, trees and water while {_button} is held; people still block the way"] = (
        f"Atraviesa paredes, árboles y agua mientras mantienes {_button}; las personas siguen bloqueando el paso")
    for _slower, _slower_es in _SLOWER.items():
        ES_EXTRA[f"The game runs {_slower} while {_button} is held, to hit the frame"] = (
            f"El juego va {_slower_es} mientras mantienes {_button}, para atinarle al fotograma")

del _n, _version, _version_es, _language, _language_es, _en, _es, _where, _where_es, _speed, _button, _slower, \
    _slower_es

# poke-app: the casino-coins card in the ready-made gifts
ES_EXTRA["Game Corner coins"] = "Monedas del Casino"
ES_EXTRA["9999 coins for the Game Corner, again whenever you need more."] = (
    "9999 monedas para el Casino, cada vez que necesites más.")

# poke-app: the Board page (gui/views/boards.py) and its firmware list (gui/board.py FIRMWARES)
ES_EXTRA["Checks and installs show their output here."] = "Aquí aparece lo que muestran las revisiones y las instalaciones."
ES_EXTRA["Look again"] = "Buscar otra vez"
ES_EXTRA["{chip} board"] = "Placa {chip}"
ES_EXTRA["ESP32 board"] = "Placa ESP32"
ES_EXTRA["pokeldn board"] = "Placa de pokeldn"
ES_EXTRA["Needs attention"] = "Requiere atención"
ES_EXTRA["Plug it into this computer with a data cable. It shows up here on its own."] = (
    "Conéctala a esta computadora con un cable de datos. Aparece aquí sola.")
ES_EXTRA["Working"] = "Trabajando"
ES_EXTRA["Installing {name} firmware"] = "Instalando el firmware {name}"
ES_EXTRA["Keep the board plugged in. About a minute."] = "Deja la placa conectada. Tarda como un minuto."
ES_EXTRA["Asking the board over Bluetooth for its firmware version."] = (
    "Preguntándole a la placa por Bluetooth la versión de su firmware.")
ES_EXTRA["Version unknown"] = "Versión desconocida"
ES_EXTRA["Install a firmware below. The Wireless firmware is the one every Games tool needs."] = (
    "Instala un firmware de abajo. El firmware Inalámbrico es el que necesita cada herramienta de Juegos.")
ES_EXTRA["Install {name}"] = "Instalar {name}"
ES_EXTRA["Update required"] = "Actualización necesaria"
ES_EXTRA["This firmware speaks an older protocol than this app. Update it to use the board."] = (
    "Este firmware usa un protocolo más viejo que esta app. Actualízalo para usar la placa.")
ES_EXTRA["Update available: {version}"] = "Actualización disponible: {version}"
ES_EXTRA["{name} firmware {version} is included with this app. This board runs {installed}."] = (
    "El firmware {name} {version} viene con esta app. Esta placa tiene la {installed}.")
ES_EXTRA["Up to date"] = "Al día"
ES_EXTRA["{name} firmware {version} is the newest this app includes."] = (
    "El firmware {name} {version} es el más nuevo que trae esta app.")
ES_EXTRA["{name} firmware."] = "Firmware {name}."
ES_EXTRA["Use for trades"] = "Usar para intercambios"
ES_EXTRA["Open Control"] = "Abrir Control"
ES_EXTRA["Installed · {version}"] = "Instalado · {version}"
ES_EXTRA["Installed"] = "Instalado"
ES_EXTRA["Not available on {chip}"] = "No disponible en {chip}"
ES_EXTRA["Install"] = "Instalar"
ES_EXTRA["Install from a file..."] = "Instalar desde un archivo..."
ES_EXTRA["This copy of the app has no firmware images (a copy run from source). Download the released ones; no "
         "ESP-IDF needed."] = (
    "Esta copia de la app no trae imágenes de firmware (se ejecuta desde el código fuente). Descarga las "
    "publicadas; no necesitas ESP-IDF.")
ES_EXTRA["A board runs one firmware at a time. Switching takes about a minute, and you can switch back whenever "
         "you like."] = (
    "Una placa usa un firmware a la vez. Cambiar tarda como un minuto, y puedes volver al otro cuando quieras.")
ES_EXTRA["Chip"] = "Chip"
ES_EXTRA["Unknown"] = "Desconocido"
ES_EXTRA["None"] = "Ninguno"
ES_EXTRA["Connection"] = "Conexión"
ES_EXTRA["USB to this computer, as a controller; Bluetooth to this app"] = (
    "USB a esta computadora, como mando; Bluetooth a esta app")
ES_EXTRA["USB serial, {bridge}"] = "USB serie, {bridge}"
ES_EXTRA["Save the name"] = "Guardar el nombre"
ES_EXTRA["About this board"] = "Acerca de esta placa"
ES_EXTRA["The board did not answer over Bluetooth ({error}). Is Bluetooth on?"] = (
    "La placa no respondió por Bluetooth ({error}). ¿Está encendido el Bluetooth?")
ES_EXTRA["It replaces the {name} firmware: the board stops working as {role} until you install {name} again."] = (
    "Reemplaza el firmware {name}: la placa deja de funcionar como {role} hasta que vuelvas a instalar {name}.")
ES_EXTRA["Keep the board plugged into this computer. It takes about a minute."] = (
    "Deja la placa conectada a esta computadora. Tarda como un minuto.")
ES_EXTRA["From the file {name}."] = "Desde el archivo {name}."
ES_EXTRA["Install {name} firmware?"] = "¿Instalar el firmware {name}?"
ES_EXTRA["Starting..."] = "Empezando..."
ES_EXTRA["Asking the board to restart for installing..."] = "Pidiéndole a la placa que se reinicie para instalar..."
ES_EXTRA["The board did not answer over Bluetooth ({error})."] = "La placa no respondió por Bluetooth ({error})."
ES_EXTRA["Waiting for the board to restart..."] = "Esperando a que la placa se reinicie..."
ES_EXTRA["The board did not come back for installing."] = "La placa no volvió para instalar."
ES_EXTRA["The install did not finish."] = "La instalación no terminó."
ES_EXTRA["Installed. Plug the board into the Switch's USB-C port and open Control."] = (
    "Instalado. Conecta la placa al puerto USB-C de la Switch y abre Control.")
ES_EXTRA["Installed. Checking the board..."] = "Instalado. Revisando la placa..."
ES_EXTRA["{why} Unplug the board, hold its BOOT button while plugging it back in, let go, then choose Install "
         "again on the board that appears. On a board with two USB ports, use the one marked USB."] = (
    "{why} Desconecta la placa, mantén su botón BOOT mientras la vuelves a conectar, suéltalo y elige Instalar "
    "otra vez en la placa que aparezca. En una placa con dos puertos USB, usa el que dice USB.")
ES_EXTRA["Use a classic ESP32 (ESP32-D0WD, WROOM-32E), or an ESP32-S3, C3 or C6 through its native USB port, the "
         "one marked USB. S2 boards are not supported."] = (
    "Usa un ESP32 clásico (ESP32-D0WD, WROOM-32E), o un ESP32-S3, C3 o C6 por su puerto USB nativo, el que dice "
    "USB. Las placas S2 no son compatibles.")
ES_EXTRA["An install stuck on Connecting: hold the board's BOOT button until writing starts."] = (
    "¿La instalación se queda en Conectando? Mantén el botón BOOT de la placa hasta que empiece a escribir.")
ES_EXTRA["A controller board is listed only while it is plugged into this computer."] = (
    "Una placa de mando solo aparece mientras está conectada a esta computadora.")
ES_EXTRA["Board not listed, or not answering?"] = "¿Tu placa no aparece o no responde?"
ES_EXTRA["Wireless"] = "Inalámbrico"
ES_EXTRA["Controller"] = "Mando"
ES_EXTRA["The board is the radio for trades, Mystery Gift and every tool on the Games page."] = (
    "La placa es la radio para intercambios, Regalo Misterioso y cada herramienta de la página Juegos.")
ES_EXTRA["The board is a controller for the Switch: this computer presses its buttons and plays macros from the "
         "Control page."] = (
    "La placa es un mando para la Switch: esta computadora presiona sus botones y reproduce macros desde la "
    "página Control.")
ES_EXTRA["the radio for trades"] = "la radio de los intercambios"
ES_EXTRA["a controller for the Switch"] = "un mando para la Switch"

# poke-app: board status lines new with the controller firmware (gui/app.py BoardStatus)
ES_EXTRA["Your board runs the Controller firmware"] = "Tu placa tiene el firmware Mando"
ES_EXTRA["Trades need the Wireless firmware: install it from the Board page."] = (
    "Los intercambios necesitan el firmware Inalámbrico: instálalo desde la página Placa.")
ES_EXTRA["Update it on the Board page."] = "Actualízalo en la página Placa."
ES_EXTRA["Install the Wireless firmware on the Board page. If you just installed it, press the board's RESET (RST) "
         "button."] = (
    "Instala el firmware Inalámbrico en la página Placa. Si acabas de instalarlo, presiona el botón RESET (RST) de "
    "la placa.")

# poke-app: the controller page (gui/views/controller.py)
ES_EXTRA["macOS refused Bluetooth to this program. The packaged app asks for it; from a source checkout, allow "
         "Bluetooth for the terminal in System Settings, Privacy & Security."] = (
    "macOS le negó el Bluetooth a este programa. La app empaquetada lo pide; desde el código fuente, permite el "
    "Bluetooth para la terminal en Configuración del Sistema, Privacidad y seguridad.")
ES_EXTRA["Not connected"] = "Sin conectar"
ES_EXTRA["Looking for the board..."] = "Buscando la placa..."
ES_EXTRA["Connected"] = "Conectada"
ES_EXTRA["Board lost: looking for it again..."] = "Se perdió la placa: buscándola otra vez..."
ES_EXTRA["Board lost: looking for it again. Is it plugged into the Switch or a USB power source?"] = (
    "Se perdió la placa: buscándola otra vez. ¿Está conectada a la Switch o a una fuente de energía USB?")
ES_EXTRA["Wait {ms} ms"] = "Esperar {ms} ms"
ES_EXTRA["Repeat {n} times"] = "Repetir {n} veces"
ES_EXTRA["left stick {direction}"] = "stick izquierdo {direction}"
ES_EXTRA["right stick {direction}"] = "stick derecho {direction}"
ES_EXTRA["{keys}  ·  {ms} ms, then {after} ms"] = "{keys}  ·  {ms} ms, luego {after} ms"
ES_EXTRA["Nothing"] = "Nada"
ES_EXTRA["Centre"] = "Centro"
ES_EXTRA["Up"] = "Arriba"
ES_EXTRA["Up-right"] = "Arriba-derecha"
ES_EXTRA["Right"] = "Derecha"
ES_EXTRA["Down-right"] = "Abajo-derecha"
ES_EXTRA["Down"] = "Abajo"
ES_EXTRA["Down-left"] = "Abajo-izquierda"
ES_EXTRA["Left"] = "Izquierda"
ES_EXTRA["Up-left"] = "Arriba-izquierda"
ES_EXTRA["Macros"] = "Macros"
ES_EXTRA["Macro"] = "Macro"
ES_EXTRA["New macro"] = "Macro nueva"
ES_EXTRA["Import a .pokemacro file"] = "Importar un archivo .pokemacro"
ES_EXTRA["Open the macros folder"] = "Abrir la carpeta de macros"
ES_EXTRA["No macros yet. Make one with +, or import a .pokemacro someone shared."] = (
    "Todavía no hay macros. Crea una con + o importa un .pokemacro que alguien compartió.")
ES_EXTRA["This file does not load: {error}"] = "Este archivo no se pudo cargar: {error}"
ES_EXTRA["Export macro"] = "Exportar macro"
ES_EXTRA["Delete this macro?"] = "¿Borrar esta macro?"
ES_EXTRA["{name} is deleted from this computer. Export it first to keep a file."] = (
    "{name} se borrará de esta computadora. Expórtala antes si quieres conservar el archivo.")
ES_EXTRA["Playing on the board. It keeps going if this computer sleeps."] = (
    "Reproduciendo en la placa. Sigue aunque esta computadora se suspenda.")
ES_EXTRA["Board connected on {port}"] = "Placa conectada en {port}"
ES_EXTRA["Board connected over Bluetooth"] = "Placa conectada por Bluetooth"
ES_EXTRA["Disconnect"] = "Desconectar"
ES_EXTRA["Stop looking"] = "Dejar de buscar"
ES_EXTRA["Looking..."] = "Buscando..."
ES_EXTRA["Connect"] = "Conectar"
ES_EXTRA["Macro running: loop {loop}, step {step} of {count}"] = "Macro en curso: vuelta {loop}, paso {step} de {count}"
ES_EXTRA["Controller board"] = "Placa de mando"
ES_EXTRA["Paired with the Switch"] = "Emparejada con la Switch"
ES_EXTRA["Not paired: on the Switch, open Controllers, Change Grip/Order"] = (
    "Sin emparejar: en la Switch, abre Controllers, Change Grip/Order")
ES_EXTRA["Plugged into this computer: plug it into the Switch to play"] = (
    "Conectada a esta computadora: conéctala a la Switch para jugar")
ES_EXTRA["Plugged into the Switch"] = "Conectada a la Switch"
ES_EXTRA["Not plugged into the Switch"] = "Sin conectar a la Switch"
ES_EXTRA["Open the Board page"] = "Abrir la página Placa"
ES_EXTRA["A controller board is plugged into this computer. Press Connect to reach it over Bluetooth. To play, plug "
         "it into the Switch's USB-C port; it reconnects on its own."] = (
    "Hay una placa de mando conectada a esta computadora. Presiona Conectar para llegar a ella por Bluetooth. Para "
    "jugar, conéctala al puerto USB-C de la Switch; se vuelve a conectar sola.")
ES_EXTRA["The board plugged in runs the wireless firmware, for trades. To use it as a controller, install the "
         "Controller firmware on the Board page."] = (
    "La placa conectada tiene el firmware Inalámbrico, para intercambios. Para usarla como mando, instala el "
    "firmware Mando en la página Placa.")
ES_EXTRA["No controller board found. An ESP32-S3 with the controller firmware plugs into the Switch's USB-C port "
         "and this computer reaches it over Bluetooth; a classic ESP32 stays plugged into this computer and pairs "
         "with the Switch as a Pro Controller. Install it on the Board page."] = (
    "No se encontró ninguna placa de mando. Un ESP32-S3 con el firmware Mando se conecta al puerto USB-C de la "
    "Switch y esta computadora llega a él por Bluetooth; un ESP32 clásico se queda conectado a esta computadora y "
    "se empareja con la Switch como un Pro Controller. Instálalo en la página Placa.")
ES_EXTRA["Left stick"] = "Stick izquierdo"
ES_EXTRA["Right stick"] = "Stick derecho"
ES_EXTRA["D-pad"] = "Cruceta"
ES_EXTRA["Keyboard"] = "Teclado"
ES_EXTRA["Arrows for the D-pad, X A, Z B, S X, A Y, Q L, W R, 1 ZL, 2 ZR, Enter +, Backspace -, H HOME, "
         "C Capture"] = (
    "Flechas para la cruceta, X A, Z B, S X, A Y, Q L, W R, 1 ZL, 2 ZR, Enter +, Retroceso -, H HOME, C Capture")
ES_EXTRA["Record into the macro"] = "Grabar en la macro"
ES_EXTRA["Each press, its length and the pause before the next one become steps"] = (
    "Cada pulsación, su duración y la pausa antes de la siguiente se vuelven pasos")
ES_EXTRA["Hold a button to hold it on the console."] = "Mantén un botón para mantenerlo en la consola."
ES_EXTRA["Pick a macro on the left, or make a new one with +."] = "Elige una macro a la izquierda o crea una nueva con +."
ES_EXTRA["Description"] = "Descripción"
ES_EXTRA["Press (ms)"] = "Pulsación (ms)"
ES_EXTRA["Pause after (ms)"] = "Pausa después (ms)"
ES_EXTRA["How long a step holds its buttons unless it says otherwise"] = (
    "Cuánto mantiene un paso sus botones, salvo que diga otra cosa")
ES_EXTRA["The pause after each step unless it says otherwise"] = "La pausa después de cada paso, salvo que diga otra cosa"
ES_EXTRA["Repeat the loop (0 = until stopped)"] = "Repetir el bucle (0 = hasta detenerla)"
ES_EXTRA["Run once"] = "Una vez"
ES_EXTRA["Loop"] = "Bucle"
ES_EXTRA["Recording here"] = "Grabando aquí"
ES_EXTRA["Record here"] = "Grabar aquí"
ES_EXTRA["Move up"] = "Subir"
ES_EXTRA["+ Press"] = "+ Pulsar"
ES_EXTRA["+ Wait"] = "+ Esperar"
ES_EXTRA["+ Repeat"] = "+ Repetir"
ES_EXTRA["Wait (ms)"] = "Espera (ms)"
ES_EXTRA["Times"] = "Veces"
ES_EXTRA["{ms}, the macro's"] = "{ms}, el de la macro"
ES_EXTRA["Buttons held together"] = "Botones presionados a la vez"
ES_EXTRA["Hold (ms)"] = "Mantener (ms)"
ES_EXTRA["What this step is for"] = "Para qué es este paso"
ES_EXTRA["Note (optional)"] = "Nota (opcional)"
ES_EXTRA["Edit step"] = "Editar paso"
ES_EXTRA["Save"] = "Guardar"
ES_EXTRA["until stopped"] = "hasta detenerla"
ES_EXTRA["{steps} of {limit} board steps  ·  run once {setup} s  ·  loop {loop} s {loops}"] = (
    "{steps} de {limit} pasos de la placa  ·  una vez {setup} s  ·  bucle {loop} s {loops}")
ES_EXTRA["Play on the board"] = "Reproducir en la placa"
ES_EXTRA["Connect the board first"] = "Primero conecta la placa"
ES_EXTRA["Export as a .pokemacro file to share"] = "Exportar como archivo .pokemacro para compartir"
ES_EXTRA["Delete this macro"] = "Borrar esta macro"

# poke-app: the bank (gui/views/bank.py)
ES_EXTRA["Bank"] = "Banco"
ES_EXTRA["Open the bank folder"] = "Abrir la carpeta del banco"
ES_EXTRA["All Pokemon"] = "Todos los Pokémon"
ES_EXTRA["The bank is empty. Every Pokemon a trade brings in lands here, from any game."] = (
    "El banco está vacío. Cada Pokémon que recibes en un intercambio llega aquí, de cualquier juego.")
ES_EXTRA["{n} Pokemon in the bank"] = "{n} Pokémon en el banco"
ES_EXTRA["{n} Pokemon from {game}"] = "{n} Pokémon de {game}"
ES_EXTRA["Pick a Pokemon to see where it can go."] = "Elige un Pokémon para ver a dónde puede ir."
ES_EXTRA["In {game}"] = "En {game}"
ES_EXTRA["Banked {when}"] = "Guardado el {when}"
ES_EXTRA["PKHeX finds it not legal"] = "PKHeX lo marca como no legal"
ES_EXTRA["Waiting to trade"] = "Esperando intercambio"
ES_EXTRA["Queued in {tools}. It leaves the bank when that trade completes."] = (
    "En cola en {tools}. Sale del banco cuando se complete ese intercambio.")
ES_EXTRA["Open the trade"] = "Abrir el intercambio"
ES_EXTRA["Take it out"] = "Sacarlo de la cola"
ES_EXTRA["Send it to a game"] = "Mandarlo a un juego"
ES_EXTRA["PKHeX is checking each game..."] = "PKHeX está revisando cada juego..."
ES_EXTRA["Its own game"] = "Su propio juego"
ES_EXTRA["Moves as HOME would move it"] = "Se mueve como lo haría HOME"
ES_EXTRA["Queue it for a {game} trade:"] = "Ponlo en cola para un intercambio de {game}:"
ES_EXTRA["Moving it to {game}..."] = "Moviéndolo a {game}..."
ES_EXTRA["Export Pokemon"] = "Exportar Pokémon"
ES_EXTRA["Remove this Pokemon?"] = "¿Quitar este Pokémon?"
ES_EXTRA["{name} is deleted from the bank on this computer. Export it first to keep a file."] = (
    "{name} se borrará del banco de esta computadora. Expórtalo antes si quieres conservar el archivo.")
# a save, a macro or a Pokemon: one wording for all three
ES_EXTRA["Exported to {path}"] = "Se exportó a {path}"
# pokeldn.app.bank.enqueue, for the trades a banked Pokemon can be queued in
for _tool, _tool_es in (("Trade (Host)", "Intercambio (anfitrión)"), ("Trade (Join)", "Intercambio (unirse)")):
    for _n in range(1, 7):
        ES_EXTRA[f"{_tool} already has {_n} Pokemon queued."] = f"{_tool_es} ya tiene {_n} Pokémon en cola."
del _tool, _tool_es, _n

# poke-app: the raid reward rows (gui/views/rewards.py)
ES_EXTRA["Add reward"] = "Agregar recompensa"
ES_EXTRA["1 to 999"] = "De 1 a 999"
ES_EXTRA["Quantity"] = "Cantidad"
ES_EXTRA["Remove reward"] = "Quitar recompensa"
ES_EXTRA["The raid's own rewards, shown with the raid above."] = (
    "Las recompensas propias de la incursión, que se muestran con la incursión de arriba.")

# poke-app: the online trade's partner (gui/views/games.py SessionPanel)
ES_EXTRA["Partner"] = "Compañero"
ES_EXTRA["Connecting to the relays"] = "Conectando con los relés"
ES_EXTRA["Looking for a partner"] = "Buscando un compañero"
ES_EXTRA["Trading with {name}"] = "Intercambiando con {name}"
ES_EXTRA["{name} left"] = "{name} se fue"
ES_EXTRA["Your partner left"] = "Tu compañero se fue"
ES_EXTRA["Anyone trading this game online without a code can be your partner."] = (
    "Cualquiera que intercambie este juego en línea sin código puede ser tu compañero.")
ES_EXTRA["Your partner enters the same code: {code}."] = "Tu compañero pone el mismo código: {code}."
ES_EXTRA["Back out of the trade on the console. Start again to find a partner."] = (
    "Sal del intercambio en la consola. Empieza otra vez para encontrar un compañero.")
ES_EXTRA["They confirmed. Confirm on your console to trade."] = "Ya confirmó. Confirma en tu consola para intercambiar."
ES_EXTRA["Waiting for them to confirm."] = "Esperando a que confirme."
ES_EXTRA["Offer a Pokemon on your console; theirs appears here once they choose."] = (
    "Ofrece un Pokémon en tu consola; el suyo aparece aquí en cuanto lo elija.")
ES_EXTRA["PKHeX flags it: {flag}"] = "PKHeX lo marca: {flag}"
ES_EXTRA["Trade {n}: {summary}"] = "Intercambio {n}: {summary}"
ES_EXTRA["Trade {n} (done): {summary}"] = "Intercambio {n} (hecho): {summary}"

# poke-app: FireRed/LeafGreen's online trade (pokeldn.app.catalog online() and ONLINE_CODE_HELP)
ES_EXTRA["Trade (Online)"] = "Intercambio (en línea)"
ES_EXTRA["Trade with a player far away: each of you hosts your own console, and the two trade through the "
         "internet."] = (
    "Intercambia con alguien lejos: cada quien conecta su propia consola y los dos intercambian por internet.")
ES_EXTRA["Agree on a code with your partner, or leave it empty to meet anyone trading online."] = (
    "Acuerda un código con tu compañero, o déjalo vacío para encontrarte con cualquiera que intercambie en línea.")
ES_EXTRA["Start, then wait for 'Trading with' and your partner's name."] = (
    "Presiona Empezar y espera a ver 'Intercambiando con' y el nombre de tu compañero.")
ES_EXTRA["Your partner's party shows on the right: choose the Pokemon you send, then confirm."] = (
    "El equipo de tu compañero aparece a la derecha: elige el Pokémon que mandas y confirma.")
ES_EXTRA["Your partner's Pokemon appears once they offer it. The trade goes through once both of you confirm."] = (
    "El Pokémon de tu compañero aparece en cuanto lo ofrece. El intercambio se hace cuando los dos confirman.")
ES_EXTRA["Code"] = "Código"
ES_EXTRA["Eight digits you and your partner agree on; you also enter them on the console. Empty meets anyone "
         "trading this game online without a code."] = (
    "Ocho dígitos que acuerdas con tu compañero; también los pones en la consola. Vacío: te encuentras con "
    "cualquiera que intercambie este juego en línea sin código.")
# the trainer reader's hidden Version field (pokeldn.app.catalog FRLG_TRAINER), on the Advanced tab
ES_EXTRA["The game pokeldn's own trainer reports on the link."] = (
    "El juego que informa el entrenador de pokeldn en la conexión.")
