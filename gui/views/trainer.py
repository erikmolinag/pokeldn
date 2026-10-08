"""The player's trainer card: the FireRed/LeafGreen trainer read from the console (pokeldn.app.received
.trainer_found) or typed in Settings. Built Pokemon carry it as their original trainer."""
import flet as ft

from gui import theme as t
from gui.i18n import tr

LANGUAGE_NAMES = {1: "Japanese", 2: "English", 3: "French", 4: "Italian", 5: "German", 7: "Spanish"}
VERSION_NAMES = {"firered": "FireRed", "leafgreen": "LeafGreen"}
VERSION_COLORS = {"firered": ("#FF6A3D", "#E3350D"), "leafgreen": ("#4CC38A", "#1E8E5A")}
BOY, GIRL = "#3B82F6", "#E8559A"


def shiny_value(tid: int, sid: int) -> int:
    """The trainer shiny value: a Pokemon is shiny for this trainer when its PID's TSV-style value matches."""
    return (tid ^ sid) >> 3


def _avatar(name: str, gender: int, size: float) -> ft.Control:
    color = GIRL if gender else BOY
    return ft.Container(t.text((name[:1] or "?").upper(), size * 0.42, t.INK, weight=ft.FontWeight.W_900),
                        width=size, height=size, border_radius=size / 2, alignment=ft.Alignment.CENTER,
                        bgcolor=color, border=ft.Border.all(3, "#FFFFFF"), shadow=t.SHADOW)


def _fact(label: str, value: str, mono: bool = False) -> ft.Control:
    return ft.Column([
        t.text(label, 11, t.MUTED, weight=ft.FontWeight.W_700),
        t.text(value, 17, t.TEXT, weight=ft.FontWeight.W_800, font_family=t.MONO if mono else None),
    ], spacing=0, tight=True)


def _read(app):
    return lambda e: app.navigate("games", tool="frlg-trainer")


def trainer_card(app, compact: bool = False) -> ft.Control:
    mine = app.settings.my_trainer
    if not mine.get("name"):
        return _empty_card(app, compact)
    name, tid, sid = mine["name"], int(mine["tid"]), int(mine["sid"])
    gender, version = int(mine.get("gender") or 0), mine.get("version") or ""
    language = tr(LANGUAGE_NAMES.get(int(mine.get("language") or 2), "English"))
    game = tr(VERSION_NAMES.get(version, "FireRed & LeafGreen"))
    top, bottom = VERSION_COLORS.get(version, VERSION_COLORS["firered"])
    sign = t.pixel_icon("female" if gender else "male", size=18, color=GIRL if gender else BOY)
    if compact:
        return ft.Container(ft.Row([
            _avatar(name, gender, 44),
            ft.Column([
                ft.Row([t.text(name, 16, t.TEXT, weight=ft.FontWeight.W_900), sign], spacing=4, tight=True),
                t.text(f"{tr('Trainer ID')} {tid:05d} · {tr('Secret ID')} {sid:05d}", 12, t.SOFT,
                       weight=ft.FontWeight.W_700),
                t.text(f"{game} · {language}", 11, t.MUTED),
            ], spacing=1, tight=True, expand=True),
        ], spacing=12), padding=14, border_radius=18, bgcolor=t.CARD, border=ft.Border.all(1, t.OUTLINE))
    source = tr("Read from your console") if mine.get("source") == "console" else tr("Typed in by hand")
    header = ft.Container(ft.Row([
        ft.Image(src="pokeball.svg", width=26, height=26),
        t.text(tr("TRAINER CARD"), 13, t.INK, weight=ft.FontWeight.W_900, expand=True),
        ft.Container(t.text(game, 11, t.INK, weight=ft.FontWeight.W_800), padding=ft.Padding(10, 4, 10, 4),
                     border_radius=12, bgcolor=ft.Colors.with_opacity(0.22, "#FFFFFF")),
    ], spacing=10), padding=ft.Padding(20, 14, 16, 14),
        gradient=ft.LinearGradient(begin=ft.Alignment.CENTER_LEFT, end=ft.Alignment.CENTER_RIGHT,
                                   colors=[bottom, top]))
    body = ft.Container(ft.Column([
        ft.Row([
            _avatar(name, gender, 72),
            ft.Column([
                t.text(name, 30, t.TEXT, weight=ft.FontWeight.W_900),
                ft.Row([sign, t.text(f"{tr('Girl') if gender else tr('Boy')} · {language}", 13, t.MUTED,
                                     weight=ft.FontWeight.W_700)], spacing=4, tight=True),
            ], spacing=0, tight=True, expand=True),
        ], spacing=16),
        ft.Container(height=1, bgcolor=t.DIVIDER),
        ft.Row([
            ft.Container(_fact(tr("Trainer ID"), f"{tid:05d}", mono=True), expand=1),
            ft.Container(_fact(tr("Secret ID"), f"{sid:05d}", mono=True), expand=1),
            ft.Container(_fact(tr("Shiny value"), f"{shiny_value(tid, sid)}", mono=True), expand=1),
        ], spacing=12),
        ft.Row([
            t.badge(source, t.GREEN if mine.get("source") == "console" else t.MUTED,
                    "checkbox-on" if mine.get("source") == "console" else "edit"),
            ft.Container(expand=True),
            t.secondary_button(tr("Edit"), lambda e: app.navigate("settings"), "edit"),
            t.button(tr("Read again"), _read(app), "refresh"),
        ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ], spacing=16, tight=True), padding=ft.Padding(20, 18, 20, 18))
    return ft.Container(ft.Column([header, body], spacing=0, tight=True), bgcolor=t.PANEL, border_radius=24,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS, border=ft.Border.all(1, t.OUTLINE),
                        shadow=t.SHADOW)


def _empty_card(app, compact: bool) -> ft.Control:
    text = tr("Connect the board, join the Direct Corner on your console and pokeldn reads your name, "
              "Trainer ID and Secret ID in seconds. Nothing is traded.")
    if compact:
        return ft.Container(ft.Row([
            t.pixel_icon("trainer", size=24, color=t.ACCENT),
            t.text(tr("No trainer yet"), 13, t.TEXT, weight=ft.FontWeight.W_800, expand=True),
            t.button(tr("Read from my console"), _read(app), "trainer"),
        ], spacing=10), padding=14, border_radius=18, bgcolor=t.CARD)
    return ft.Container(ft.Column([
        ft.Row([
            ft.Container(ft.Image(src="pokeball.svg", width=40, height=40), width=64, height=64,
                         border_radius=32, bgcolor=t.SELECTED, alignment=ft.Alignment.CENTER),
            ft.Column([t.text(tr("No trainer yet"), 22, t.TEXT, weight=ft.FontWeight.W_900),
                       t.text(tr("Your trainer card"), 13, t.MUTED, weight=ft.FontWeight.W_700)],
                      spacing=0, tight=True, expand=True),
        ], spacing=16),
        t.text(text, 14, t.SOFT),
        ft.Row([t.button(tr("Read from my console"), _read(app), "trainer"),
                t.secondary_button(tr("Edit"), lambda e: app.navigate("settings"), "edit")], spacing=8),
    ], spacing=16, tight=True), padding=24, bgcolor=t.PANEL, border_radius=24, border=ft.Border.all(1, t.OUTLINE),
        shadow=t.SHADOW)
