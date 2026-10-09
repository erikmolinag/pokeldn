"""poke-app's main menu, laid out like Pokemon HOME's: the player's trainer card on the left with the team ready to
trade in box cells, and the menu as rounded tiles on the right, Trade the big gradient one. Arrows move the mint
cursor between the tiles, Enter opens the selected one."""
import flet as ft

from gui import theme as t
from gui.i18n import tr
from gui.views.sprites import Sprite
from gui.views.trainer import BOY, GIRL, LANGUAGE_NAMES, VERSION_NAMES, shiny_value
from pokeldn.app import command

# (screen key, icon, title, detail, tile shape)
ENTRIES = (
    ("trade", "arrows-horizontal", "Trade", "Send a Pokemon built for your save, or receive one.", "hero"),
    ("gift", "gift", "Mystery Gift", "Eggs, items and events", "wide"),
    ("team", "pokeball", "Pokemon", "Build Pokemon for your save", "wide"),
    ("trainer", "trainer", "My trainer", "Read your TID and SID", "small"),
    ("save", "save", "My save", "Back up and restore", "small"),
    ("bank", "package", "Bank", "Keep Pokemon between games", "small"),
    ("options", "gear", "Options", "Board, language and keys", "small"),
)
# Where each arrow moves the cursor: Trade fills the first row's left, Mystery Gift and Pokemon are stacked on its
# right, and the other four share the second row.
MOVES = {
    0: {"Arrow Right": 1, "Arrow Down": 3},
    1: {"Arrow Left": 0, "Arrow Down": 2},
    2: {"Arrow Left": 0, "Arrow Up": 1, "Arrow Down": 5},
    3: {"Arrow Up": 0, "Arrow Right": 4},
    4: {"Arrow Up": 0, "Arrow Left": 3, "Arrow Right": 5},
    5: {"Arrow Up": 2, "Arrow Left": 4, "Arrow Right": 6},
    6: {"Arrow Up": 2, "Arrow Left": 5},
}
KEYS = {"W": "Arrow Up", "S": "Arrow Down"}
TRAINER_WIDTH = 410
WHITE_SOFT = ft.Colors.with_opacity(0.92, "#FFFFFF")


class Tile:
    """One menu button: white with a gradient badge, or the big gradient one. The cursor frames the selected."""

    def __init__(self, icon: str, title: str, detail: str, shape: str, on_open, on_hover):
        hero = shape == "hero"
        name = t.text(tr(title), 34 if hero else 21 if shape == "wide" else 19, t.INK if hero else t.TEXT,
                      weight=ft.FontWeight.W_900, max_lines=1)
        about = t.text(tr(detail), 15 if hero else 13, WHITE_SOFT if hero else t.MUTED, weight=ft.FontWeight.W_600,
                       max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)
        if hero:
            body = ft.Stack([
                ft.Container(ft.Image(src="ring.svg", width=330, height=330, opacity=0.16), right=-80, bottom=-110),
                ft.Container(ft.Column([
                    ft.Container(t.pixel_icon(icon, size=40, color=t.INK), width=80, height=80, border_radius=40,
                                 bgcolor=ft.Colors.with_opacity(0.22, "#FFFFFF"), alignment=ft.Alignment.CENTER),
                    ft.Container(expand=True),
                    name, about,
                ], spacing=4), padding=ft.Padding(30, 28, 30, 26), left=0, top=0, right=0, bottom=0),
            ], expand=True)
        elif shape == "wide":
            body = ft.Container(ft.Row([
                t.badge_icon(icon, 58, 28),
                ft.Column([name, about], spacing=2, tight=True, expand=True),
                t.pixel_icon("chevron-right", size=28, color=t.FAINT),
            ], spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.Padding(22, 0, 16, 0))
        else:
            body = ft.Container(ft.Column([t.badge_icon(icon, 52, 26), ft.Container(expand=True), name, about],
                                          spacing=2), padding=ft.Padding(20, 20, 18, 18))
        self.control = ft.Container(body, border_radius=28, bgcolor=None if hero else t.PANEL,
                                    gradient=t.gradient() if hero else None, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                    on_click=lambda e: on_open(),
                                    on_hover=lambda e: on_hover() if e.data in (True, "true") else None,
                                    animate_scale=ft.Animation(140, ft.AnimationCurve.EASE_OUT), scale=1)
        self.paint(False)

    def paint(self, selected: bool) -> None:
        # The frame is always 4 px wide, see-through when not selected, so the selection never moves the content.
        self.control.border = ft.Border.all(4, t.CURSOR if selected else ft.Colors.TRANSPARENT)
        self.control.shadow = [t.GLOW, t.SHADOW] if selected else t.SHADOW
        self.control.scale = 1.025 if selected else 1


class MenuView:
    def __init__(self, app):
        self.app = app
        self.selected = 0
        self.visible = False
        self.tiles = [Tile(icon, title, detail, shape, lambda k=key: app.navigate(k), lambda i=i: self.select(i))
                      for i, (key, icon, title, detail, shape) in enumerate(ENTRIES)]
        trade, gift, team, *small = [tile.control for tile in self.tiles]
        trade.expand, gift.expand, team.expand = 5, 1, 1
        for tile in small:
            tile.expand = 1
        stretch = ft.CrossAxisAlignment.STRETCH
        grid = ft.Column([
            ft.Row([trade, ft.Column([gift, team], spacing=20, expand=4)], spacing=20, expand=3,
                   vertical_alignment=stretch),
            ft.Row(small, spacing=20, expand=2, vertical_alignment=stretch),
        ], spacing=20, expand=True)
        self.card = ft.Container(width=TRAINER_WIDTH)
        self.control = ft.Row([self.card, grid], spacing=28, expand=True, vertical_alignment=stretch)
        app.trainer_listeners.append(self._changed)
        self.render()

    # navigation

    def enter(self, **_) -> None:
        self.visible = True
        self.render()
        self.app.check_if_unknown()

    def leave(self) -> None:
        self.visible = False

    def key(self, key: str) -> bool:
        """Arrow keys move the cursor, Enter opens the selected tile (gui/main.py routes keys here)."""
        key = KEYS.get(key, key)
        if key in ("Enter", " ", "A"):
            self.app.navigate(ENTRIES[self.selected][0])
            return True
        target = MOVES[self.selected].get(key)
        if target is None:
            return key.startswith("Arrow")
        self.select(target)
        return True

    def select(self, index: int) -> None:
        if index == self.selected:
            return
        self.selected = index
        for i, tile in enumerate(self.tiles):
            tile.paint(i == index)
        self.control.update()

    def _changed(self) -> None:
        if self.visible:
            self.render()
            self.control.update()

    # drawing

    def render(self) -> None:
        for i, tile in enumerate(self.tiles):
            tile.paint(i == self.selected)
        self.card.content = self.trainer_card()

    def trainer_card(self) -> ft.Control:
        """HOME's profile: a gradient band, the avatar over its edge, the IDs and the team in box cells."""
        mine = self.app.settings.my_trainer
        known = bool(mine.get("name"))
        name, gender = (mine["name"], int(mine.get("gender") or 0)) if known else (tr("Trainer"), 0)
        avatar = ft.Container(t.text((name[:1] or "?").upper() if known else "?", 46, t.INK,
                                     weight=ft.FontWeight.W_900),
                              width=108, height=108, border_radius=54, alignment=ft.Alignment.CENTER,
                              bgcolor=(GIRL if gender else BOY) if known else t.FAINT,
                              border=ft.Border.all(5, "#FFFFFF"), shadow=t.SHADOW)
        band = ft.Container(ft.Stack([
            ft.Container(ft.Image(src="ring.svg", width=230, height=230, opacity=0.18), right=-56, top=-70),
            ft.Container(ft.Row([ft.Image(src="pokeball.svg", width=22, height=22),
                                 t.text(tr("TRAINER CARD"), 13, t.INK, weight=ft.FontWeight.W_900)], spacing=8),
                         left=24, top=20),
        ]), left=0, top=0, right=0, height=120, gradient=t.gradient(ft.Alignment.CENTER_LEFT,
                                                                       ft.Alignment.CENTER_RIGHT))
        if known:
            tid, sid = int(mine["tid"]), int(mine["sid"])
            game = tr(VERSION_NAMES.get(mine.get("version") or "", "FireRed"))
            language = tr(LANGUAGE_NAMES.get(int(mine.get("language") or 2), "English"))
            sub = ft.Row([t.pixel_icon("female" if gender else "male", size=17, color=GIRL if gender else BOY),
                          t.text(f"{tr('Girl') if gender else tr('Boy')} · {game} · {language}", 14, t.MUTED,
                                 weight=ft.FontWeight.W_700)], spacing=3, tight=True)
            facts = ft.Row([self._fact(tr("TRAINER ID"), f"{tid:05d}"), self._fact(tr("SECRET ID"), f"{sid:05d}"),
                            self._fact(tr("SHINY VALUE"), str(shiny_value(tid, sid)))], spacing=10)
        else:
            sub = t.text(tr("Your trainer is not read yet"), 14, t.MUTED, weight=ft.FontWeight.W_700)
            facts = ft.Container(ft.Column([
                t.text(tr("Read your name, Trainer ID and Secret ID from the console."), 14, t.SOFT),
                t.button(tr("Read now"), lambda e: self.app.navigate("trainer"), "trainer"),
            ], spacing=12, tight=True), padding=16, border_radius=18, bgcolor=t.CARD)
        head = ft.Stack([
            band,
            ft.Container(avatar, left=22, top=66),
            ft.Container(ft.Column([t.text(name, 30, weight=ft.FontWeight.W_900, max_lines=1), sub], spacing=0,
                                   tight=True), left=146, top=126, right=12),
        ], height=196)
        cells = self.team_slots()
        # Two rows of three box cells that share the card's remaining height, as a HOME box fills its screen.
        box = ft.Column([ft.Row(cells[i:i + 3], spacing=10, expand=1, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
                         for i in (0, 3)], spacing=10, expand=True)
        rows: list[ft.Control] = [facts, ft.Container(height=2),
                                  t.text(tr("READY TO TRADE"), 12, t.MUTED, weight=ft.FontWeight.W_900), box]
        if known:
            rows.append(ft.Row([
                t.secondary_button(tr("Edit"), lambda e: self.app.navigate("options", tab="settings"), "edit",
                                   expand=True),
                t.button(tr("Read again"), lambda e: self.app.navigate("trainer"), "refresh", expand=True),
            ], spacing=10))
        return t.glass(ft.Column([
            head,
            ft.Container(ft.Column(rows, spacing=12, expand=True), padding=ft.Padding(22, 4, 22, 22), expand=True),
        ], spacing=0, expand=True), radius=30)

    @staticmethod
    def _fact(label: str, value: str) -> ft.Control:
        return ft.Container(ft.Column([t.text(label, 10, t.MUTED, weight=ft.FontWeight.W_900, max_lines=1),
                                       t.text(value, 24, t.TEXT, weight=ft.FontWeight.W_900)], spacing=0, tight=True),
                            expand=1, padding=ft.Padding(14, 10, 10, 10), border_radius=16, bgcolor=t.CARD)

    def team_slots(self) -> list[ft.Control]:
        """The Pokemon queued on Trade (Host), as six cells of a HOME box."""
        values = self.app.settings.tool_values.get("frlg-trade-host", {}).get("values", {})
        field = next((f for f in _trade_tool().fields if f.kind == "pokemon"), None)
        offers = [o for o in command.offers(command.value_of(field, values))[:6] if o.get("file")] if field else []
        slots = []
        for offer in offers:
            sprite = Sprite(self.app, int(offer.get("species") or 0), bool(offer.get("shiny")), size=64)
            sprite.frame.bgcolor, sprite.frame.border = None, None
            slots.append(self._cell(sprite.control, offer.get("summary") or None))
        while len(slots) < 6:
            first_free = len(slots) == len(offers)
            slots.append(self._cell(t.pixel_icon("plus", size=22, color=t.FAINT) if first_free else None, None))
        return slots

    def _cell(self, content, tip) -> ft.Control:
        return ft.Container(content, expand=1, border_radius=16, bgcolor=t.CARD, alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(1, t.OUTLINE), clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            tooltip=tip, on_click=lambda e: self.app.navigate("team"))


def _trade_tool():
    from pokeldn.app.catalog import APP_GAMES
    return next(x for x in APP_GAMES[0].tools if x.key == "frlg-trade-host")
