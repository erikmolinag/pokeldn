#!/usr/bin/env python3
"""poke-app: draw the app icon (a Poke Ball, as gui/assets/pokeball.svg) into icon.png (1024) and icon.ico
(16 to 256), supersampled for smooth edges. Run once after changing the design: python scripts/make_pokeball_icon.py"""
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "gui" / "assets"
INK, RED, RED_LIGHT, WHITE, WHITE_SHADE = "#1C2333", "#E3350D", "#FF5A36", "#FFFFFF", "#E9EDF3"


def draw(size: int) -> Image.Image:
    scale = 4
    s = size * scale
    image = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    unit = s / 100   # the SVG's 100-unit box

    def box(cx, cy, r):
        return [(cx - r) * unit, (cy - r) * unit, (cx + r) * unit, (cy + r) * unit]

    # top half red, bottom half white; the band stays inside the ring, which is drawn over its ends
    d.pieslice(box(50, 50, 46), 180, 360, fill=RED_LIGHT)
    d.pieslice(box(50, 50, 46), 0, 180, fill=WHITE)
    d.rectangle([6 * unit, 46 * unit, 94 * unit, 54 * unit], fill=INK)
    d.ellipse(box(50, 50, 46), outline=INK, width=round(6 * unit))
    d.ellipse(box(50, 50, 15), fill=INK)
    d.ellipse(box(50, 50, 9), fill=WHITE)
    d.ellipse(box(50, 50, 5.5), outline="#D8DEE7", width=max(1, round(1.5 * unit)))
    return image.resize((size, size), Image.LANCZOS)


def main() -> None:
    draw(1024).save(ASSETS / "icon.png")
    draw(256).save(ASSETS / "icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128),
                                                (256, 256)])
    print("wrote", ASSETS / "icon.png", ASSETS / "icon.ico")


if __name__ == "__main__":
    main()
