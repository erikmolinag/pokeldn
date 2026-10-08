"""poke-app's home page: the player's trainer card first, then what they can do with it."""
import flet as ft

from gui import theme as t
from gui.i18n import tr
from gui.views.trainer import trainer_card


class HomeView:
    def __init__(self, app):
        self.app = app
        self.greeting = ft.Column(spacing=2, tight=True)
        self.card = ft.Container()
        self.notes = ft.Container()
        self.board = ft.Container()
        actions = ft.Column([
            self._action("arrows-horizontal", "Trade", "Send a Pokemon built for your save, or receive one.",
                         lambda e: app.navigate("games", tool="frlg-trade-host")),
            self._action("gift", "Mystery Gift", "Items, eggs, event Pokemon and game boosts.",
                         lambda e: app.navigate("games", tool="frlg-gift")),
            self._action("save", "Back up your save", "Copy your whole save to this computer.",
                         lambda e: app.navigate("games", tool="frlg-gift")),
        ], spacing=10)
        left = ft.ListView([self.greeting, self.card, self.notes], spacing=t.GAP + 4, expand=True,
                           padding=ft.Padding(28, 26, 28, 26))
        right = ft.ListView([t.text(tr("What do you want to do?"), 17, weight=ft.FontWeight.W_900), actions,
                             ft.Container(height=4), t.text(tr("Your board"), 17, weight=ft.FontWeight.W_900),
                             self.board],
                            spacing=12, expand=True, padding=ft.Padding(22, 26, 22, 26))
        self.control = ft.Row([
            t.panel(left, expand=True),
            t.panel(right, width=400),
        ], spacing=t.GAP, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
        app.trainer_listeners.append(self._changed)
        app.board_listeners.append(self._changed)
        self.render()

    def enter(self, **_) -> None:
        self.visible = True
        self.render()
        self.app.check_if_unknown()

    def leave(self) -> None:
        self.visible = False

    visible = False

    def _changed(self) -> None:
        if self.visible:
            self.render()
            self.control.update()

    def render(self) -> None:
        mine = self.app.settings.my_trainer
        self.greeting.controls = [
            t.text(tr("Hello, {name}!", name=mine["name"]) if mine.get("name") else tr("Welcome, trainer!"),
                   30, weight=ft.FontWeight.W_900),
            t.text(tr("FireRed & LeafGreen"), 14, t.MUTED, weight=ft.FontWeight.W_700),
        ]
        self.card.content = trainer_card(self.app)
        self.notes.content = t.card(tr("Your trainer card"), ft.Column([
            ft.Row([t.pixel_icon("pokeball", size=22, color=t.ACCENT), t.text(tr(
                "Every Pokemon you build here carries this trainer as its original trainer: the game treats it "
                "as caught in your own save, so it obeys at any level and shows your name."), 13, t.SOFT,
                expand=True)], spacing=12, vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([t.pixel_icon("zap", size=22, color=t.AMBER), t.text(tr(
                "Shiny Pokemon are built for your Trainer ID and Secret ID, so they are shiny in your game."),
                13, t.SOFT, expand=True)], spacing=12, vertical_alignment=ft.CrossAxisAlignment.START),
        ], spacing=12))
        status = self.app.board_status()
        color = t.GREEN if status.ready else t.INFO if status.state == "checking" else t.AMBER
        self.board.content = ft.Container(ft.Row([
            ft.Container(t.pixel_icon("cpu", size=22, color=t.INK), width=44, height=44, border_radius=22,
                         bgcolor=color, alignment=ft.Alignment.CENTER),
            ft.Column([t.text(tr(status.title), 14, weight=ft.FontWeight.W_800),
                       t.text(tr(status.detail), 12, t.MUTED)], spacing=1, tight=True, expand=True),
            t.secondary_button(tr("Board"), lambda e: self.app.navigate("board")),
        ], spacing=12), padding=16, border_radius=20, bgcolor=t.CARD, border=ft.Border.all(1, t.OUTLINE))

    def _action(self, icon: str, title: str, detail: str, on_click) -> ft.Control:
        return ft.Container(ft.Row([
            ft.Container(t.pixel_icon(icon, size=24, color=t.INK), width=48, height=48, border_radius=24,
                         bgcolor=t.ACCENT, alignment=ft.Alignment.CENTER),
            ft.Column([t.text(tr(title), 15, weight=ft.FontWeight.W_900),
                       t.text(tr(detail), 12, t.MUTED)], spacing=1, tight=True, expand=True),
            t.pixel_icon("chevron-right", size=24, color=t.FAINT),
        ], spacing=14), padding=14, border_radius=20, bgcolor=t.CARD, border=ft.Border.all(1, t.OUTLINE),
            on_click=on_click, ink=True)
