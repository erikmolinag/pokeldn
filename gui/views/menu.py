"""poke-app's main menu, in the spirit of a modern Pokemon game's pause menu: the player's trainer card and the
team ready to trade on the left, large slanted menu entries on the right. Arrows move, Enter opens."""
import flet as ft
import flet.canvas as cv

from gui import theme as t
from gui.i18n import tr
from gui.views.sprites import SIZE, Sprite
from gui.views.trainer import BOY, GIRL, LANGUAGE_NAMES, VERSION_NAMES, shiny_value
from pokeldn.app import command

# (screen key, icon, title, detail)
ENTRIES = (
    ("trade", "arrows-horizontal", "TRADE", "Send or receive Pokemon"),
    ("gift", "gift", "MYSTERY GIFT", "Eggs, items and events"),
    ("team", "pokeball", "POKEMON", "Build Pokemon for your save"),
    ("trainer", "trainer", "MY TRAINER", "Read your TID and SID"),
    ("save", "save", "MY SAVE", "Back up and restore"),
    ("options", "gear", "OPTIONS", "Board, language and keys"),
)

ITEM_W, ITEM_H, SKEW = 540, 84, 22


class MenuItem:
    """A slanted menu entry: white and pushed out when selected, translucent violet otherwise."""

    def __init__(self, icon: str, title: str, detail: str, on_open, on_hover):
        self.icon_name = icon
        self.canvas = cv.Canvas([], width=ITEM_W, height=ITEM_H)
        self.icon = ft.Container(width=52, height=52, border_radius=26, alignment=ft.Alignment.CENTER)
        self.title = t.text(tr(title), 25, weight=ft.FontWeight.W_800)
        self.detail = t.text(tr(detail), 14, weight=ft.FontWeight.W_500)
        content = ft.Container(ft.Row([self.icon, ft.Column([self.title, self.detail], spacing=0, tight=True)],
                                      spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                               padding=ft.Padding(SKEW + 24, 0, 24, 0), alignment=ft.Alignment.CENTER_LEFT,
                               width=ITEM_W, height=ITEM_H)
        self.control = ft.Container(ft.Stack([self.canvas, content], width=ITEM_W, height=ITEM_H),
                                    width=ITEM_W, height=ITEM_H, on_click=lambda e: on_open(),
                                    on_hover=lambda e: on_hover() if e.data in (True, "true") else None,
                                    animate_offset=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
                                    offset=ft.Offset(0, 0))
        self.paint(False)

    def paint(self, selected: bool) -> None:
        fill = t.HIGHLIGHT if selected else ft.Colors.with_opacity(0.55, "#140A3A")
        edge = t.HIGHLIGHT if selected else ft.Colors.with_opacity(0.22, "#FFFFFF")
        shape = [cv.Path.MoveTo(SKEW, 0), cv.Path.LineTo(ITEM_W, 0), cv.Path.LineTo(ITEM_W - SKEW, ITEM_H),
                 cv.Path.LineTo(0, ITEM_H), cv.Path.Close()]
        self.canvas.shapes = [
            cv.Path(shape, paint=ft.Paint(color=fill, style=ft.PaintingStyle.FILL)),
            cv.Path(shape, paint=ft.Paint(color=edge, stroke_width=2, style=ft.PaintingStyle.STROKE)),
        ]
        self.title.color = t.HIGHLIGHT_TEXT if selected else t.TEXT
        self.detail.color = "#5B4A9E" if selected else t.MUTED
        self.icon.bgcolor = t.ACCENT if selected else ft.Colors.with_opacity(0.16, "#FFFFFF")
        self.icon.content = t.pixel_icon(self.icon_name, size=26, color=t.INK)
        self.control.offset = ft.Offset(-0.045, 0) if selected else ft.Offset(0, 0)


class MenuView:
    def __init__(self, app):
        self.app = app
        self.selected = 0
        self.visible = False
        self.items = [MenuItem(icon, title, detail, lambda k=key: app.navigate(k),
                               lambda i=i: self.select(i))
                      for i, (key, icon, title, detail) in enumerate(ENTRIES)]
        self.card = ft.Container()
        self.board = ft.Container()
        self.control = ft.Row([
            ft.Column([self.card, ft.Container(expand=True), self.board], spacing=0, width=560),
            ft.Container(expand=True),
            ft.Column([item.control for item in self.items], spacing=12,
                      alignment=ft.MainAxisAlignment.CENTER),
        ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
        app.trainer_listeners.append(self._changed)
        app.board_listeners.append(self._changed)
        self.render()

    # navigation

    def enter(self, **_) -> None:
        self.visible = True
        self.render()
        self.app.check_if_unknown()

    def leave(self) -> None:
        self.visible = False

    def key(self, key: str) -> bool:
        """Arrow keys move the selection, Enter opens it (gui/main.py routes keys here)."""
        if key in ("Arrow Down", "S"):
            self.select((self.selected + 1) % len(self.items))
        elif key in ("Arrow Up", "W"):
            self.select((self.selected - 1) % len(self.items))
        elif key in ("Enter", " ", "A"):
            self.app.navigate(ENTRIES[self.selected][0])
        else:
            return False
        return True

    def select(self, index: int) -> None:
        if index == self.selected:
            return
        self.selected = index
        for i, item in enumerate(self.items):
            item.paint(i == index)
        self.control.update()

    def _changed(self) -> None:
        if self.visible:
            self.render()
            self.control.update()

    # drawing

    def render(self) -> None:
        for i, item in enumerate(self.items):
            item.paint(i == self.selected)
        self.card.content = self.trainer_card()
        status = self.app.board_status()
        color = t.GREEN if status.ready else t.AMBER if status.state != "checking" else t.INFO
        label = tr("Board ready on {port}", port=status.port) if status.ready else tr(status.title)
        self.board.content = ft.Container(ft.Row([
            ft.Container(width=12, height=12, border_radius=6, bgcolor=color),
            t.text(label, 15, t.TEXT, weight=ft.FontWeight.W_700),
        ], spacing=10), on_click=lambda e: self.app.navigate("options", tab="board"), padding=ft.Padding(4, 0, 0, 0))

    def trainer_card(self) -> ft.Control:
        mine = self.app.settings.my_trainer
        if mine.get("name"):
            name, gender = mine["name"], int(mine.get("gender") or 0)
            tid, sid = int(mine["tid"]), int(mine["sid"])
            game = tr(VERSION_NAMES.get(mine.get("version") or "", "FireRed"))
            language = tr(LANGUAGE_NAMES.get(int(mine.get("language") or 2), "English"))
            sub = ft.Row([t.pixel_icon("female" if gender else "male", size=18, color=t.TEXT),
                          t.text(f"{tr('Girl') if gender else tr('Boy')} · {game} · {language}", 17, t.SOFT,
                                 weight=ft.FontWeight.W_600)], spacing=4, tight=True)
            ids = ft.Row([self._id(tr("TRAINER ID"), f"{tid:05d}"), self._id(tr("SECRET ID"), f"{sid:05d}"),
                          self._id(tr("SHINY VALUE"), str(shiny_value(tid, sid)))], spacing=12)
        else:
            name, gender = tr("Trainer"), 0
            sub = t.text(tr("Your trainer is not read yet"), 17, t.SOFT, weight=ft.FontWeight.W_600)
            ids = ft.Container(ft.Row([
                t.text(tr("Read your name, Trainer ID and Secret ID from the console."), 14, t.SOFT, expand=True),
                t.button(tr("Read now"), lambda e: self.app.navigate("trainer"), "trainer"),
            ], spacing=12), padding=ft.Padding(16, 12, 12, 12), border_radius=18, bgcolor=t.CARD)
        avatar = ft.Container(t.text((name[:1] or "?").upper(), 50, t.INK, weight=ft.FontWeight.W_900),
                              width=112, height=112, border_radius=56, alignment=ft.Alignment.CENTER,
                              bgcolor=GIRL if gender else BOY, border=ft.Border.all(6, "#FFFFFF"))
        return t.glass(ft.Container(ft.Column([
            ft.Row([avatar, ft.Column([t.text(name, 46, weight=ft.FontWeight.W_900), sub], spacing=4, tight=True,
                                      expand=True)], spacing=22),
            ids,
            t.text(tr("READY TO TRADE"), 14, t.SOFT, weight=ft.FontWeight.W_800),
            ft.Row(self.team_slots(), spacing=10),
        ], spacing=20, tight=True), padding=ft.Padding(30, 28, 30, 28)), radius=30)

    def _id(self, label: str, value: str) -> ft.Control:
        return ft.Container(ft.Column([t.text(label, 12, t.MUTED, weight=ft.FontWeight.W_700),
                                       t.text(value, 28, weight=ft.FontWeight.W_900)], spacing=0, tight=True),
                            expand=1, padding=ft.Padding(16, 10, 16, 10), border_radius=16, bgcolor=t.CARD)

    def team_slots(self) -> list[ft.Control]:
        """The Pokemon queued on Trade (Host), as the six circles of a party."""
        values = self.app.settings.tool_values.get("frlg-trade-host", {}).get("values", {})
        field = next((f for f in _trade_tool().fields if f.kind == "pokemon"), None)
        offers = [o for o in command.offers(command.value_of(field, values))[:6] if o.get("file")] if field else []
        slots = []
        for offer in offers:
            sprite = Sprite(self.app, int(offer.get("species") or 0), bool(offer.get("shiny")), size=SIZE)
            sprite.frame.bgcolor, sprite.frame.border = None, None
            slots.append(ft.Container(sprite.control, width=78, height=78, border_radius=39, bgcolor=t.CARD,
                                      clip_behavior=ft.ClipBehavior.ANTI_ALIAS, alignment=ft.Alignment.CENTER,
                                      tooltip=offer.get("summary") or None,
                                      on_click=lambda e: self.app.navigate("team")))
        while len(slots) < 6:
            slots.append(ft.Container(t.pixel_icon("plus", size=22, color=t.FAINT) if len(slots) == len(offers)
                                      else None, width=78, height=78, border_radius=39, bgcolor=t.CARD,
                                      alignment=ft.Alignment.CENTER, on_click=lambda e: self.app.navigate("team")))
        return slots


def _trade_tool():
    from pokeldn.app.catalog import APP_GAMES
    return next(x for x in APP_GAMES[0].tools if x.key == "frlg-trade-host")
