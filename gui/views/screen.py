"""poke-app's full screens: each menu entry opens one, with a game-style header (B to go back, the entry's icon
and title) over the tool it holds."""
import flet as ft

from gui import theme as t
from gui.i18n import tr


def key_chip(letter: str) -> ft.Control:
    """A controller face button, as the game's prompts draw them; "↕" draws the up/down arrows."""
    inner = (t.pixel_icon("unfold", size=20, color=t.HIGHLIGHT_TEXT) if letter == "↕" else
             t.text(letter, 15, t.HIGHLIGHT_TEXT, weight=ft.FontWeight.W_900))
    return ft.Container(inner, width=30, height=30, border_radius=15, bgcolor=t.HIGHLIGHT,
                        alignment=ft.Alignment.CENTER)


def header(app, icon: str, title: str, detail: str) -> ft.Control:
    back = ft.Container(ft.Row([key_chip("B"), t.text(tr("Back"), 16, weight=ft.FontWeight.W_800)], spacing=10,
                               tight=True),
                        padding=ft.Padding(8, 8, 18, 8), border_radius=24, bgcolor=t.PANEL,
                        border=ft.Border.all(2, t.OUTLINE), on_click=lambda e: app.back(),
                        tooltip=tr("Back to the menu (Esc)"))
    return ft.Row([
        back,
        ft.Container(t.pixel_icon(icon, size=30, color=t.INK), width=58, height=58, border_radius=29,
                     bgcolor=t.ACCENT, alignment=ft.Alignment.CENTER, border=ft.Border.all(3, "#FFFFFF")),
        ft.Column([t.text(tr(title), 34, weight=ft.FontWeight.W_900),
                   t.text(tr(detail), 15, t.SOFT, weight=ft.FontWeight.W_600)], spacing=0, tight=True),
    ], spacing=18, vertical_alignment=ft.CrossAxisAlignment.CENTER)


class ScreenView:
    """A menu entry's screen around an inner view (a GamesView, Settings...), passing enter/leave through."""

    def __init__(self, app, icon: str, title: str, detail: str, inner, enter_args: dict | None = None,
                 side: ft.Control | None = None):
        self.app, self.inner, self.enter_args = app, inner, enter_args or {}
        body = inner.control if side is None else ft.Row([inner.control, side], spacing=t.GAP, expand=True,
                                                         vertical_alignment=ft.CrossAxisAlignment.STRETCH)
        self.control = ft.Column([header(app, icon, title, detail), ft.Container(body, expand=True)], spacing=18,
                                 expand=True)

    def enter(self, **kwargs) -> None:
        if hasattr(self.inner, "enter"):
            self.inner.enter(**{**self.enter_args, **kwargs})

    def leave(self) -> None:
        if hasattr(self.inner, "leave"):
            self.inner.leave()


class OptionsView:
    """Settings, the board and the guide on one screen, switched by tabs."""

    TABS = (("settings", "Settings", "gear"), ("board", "Board", "cpu"), ("docs", "Guide", "book-open"))

    def __init__(self, app):
        from gui.views.boards import BoardView
        from gui.views.docs import DocsView
        from gui.views.settings import SettingsView
        self.app = app
        self.views = {"settings": SettingsView(app), "board": BoardView(app), "docs": DocsView(app)}
        self.tab = "settings"
        self.tabs = ft.Container()
        self.body = ft.Container(expand=True)
        self.control = ft.Column([
            ft.Row([t.glass(ft.Container(self.tabs, padding=4), radius=22)], alignment=ft.MainAxisAlignment.START),
            self.body,
        ], spacing=14, expand=True)
        self.render()

    def render(self) -> None:
        self.tabs.content = t.segmented([(k, tr(label), icon) for k, label, icon in self.TABS], self.tab, self.pick)
        self.body.content = self.views[self.tab].control

    def pick(self, tab: str) -> None:
        self.show(tab)
        self.control.update()

    def show(self, tab: str, **kwargs) -> None:
        old = self.views.get(self.tab)
        if tab != self.tab and hasattr(old, "leave"):
            old.leave()
        self.tab = tab if tab in self.views else "settings"
        self.render()
        view = self.views[self.tab]
        if hasattr(view, "enter"):
            view.enter(**kwargs)

    def enter(self, tab: str = "", **kwargs) -> None:
        self.show(tab or self.tab, **kwargs)

    def leave(self) -> None:
        view = self.views.get(self.tab)
        if hasattr(view, "leave"):
            view.leave()
