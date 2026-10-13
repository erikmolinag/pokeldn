"""poke-app's full screens: each menu entry opens one. As in HOME, the top bar names the screen and holds the way
back (gui/main.py draws it); the screen itself is the tool it holds."""
import flet as ft

from gui import theme as t
from gui.i18n import tr


def key_chip(letter: str) -> ft.Control:
    """A controller face button, as the game's prompts draw them; "↕" draws the up/down arrows."""
    inner = (t.pixel_icon("unfold", size=18, color=t.HIGHLIGHT_TEXT) if letter == "↕" else
             t.text(letter, 13, t.HIGHLIGHT_TEXT, weight=ft.FontWeight.W_900))
    return ft.Container(inner, width=26, height=26, border_radius=13, bgcolor=t.HIGHLIGHT,
                        alignment=ft.Alignment.CENTER)


class ScreenView:
    """A menu entry's screen around an inner view (a GamesView, Settings...), passing enter/leave through."""

    def __init__(self, app, icon: str, title: str, detail: str, inner, enter_args: dict | None = None,
                 side: ft.Control | None = None):
        self.app, self.inner, self.enter_args = app, inner, enter_args or {}
        self.icon, self.title, self.detail = icon, title, detail
        body = inner.control if side is None else ft.Row([inner.control, side], spacing=t.GAP, expand=True,
                                                         vertical_alignment=ft.CrossAxisAlignment.STRETCH)
        self.control = ft.Container(body, expand=True)

    def enter(self, **kwargs) -> None:
        if hasattr(self.inner, "enter"):
            self.inner.enter(**{**self.enter_args, **kwargs})

    def leave(self) -> None:
        if hasattr(self.inner, "leave"):
            self.inner.leave()


class TabsView:
    """A few pages on one screen, switched by tabs; the first tab is the screen's own page."""

    TABS: tuple = ()   # (key, label, icon)

    def __init__(self, app, views: dict):
        self.app = app
        self.views = views
        self.tab = self.TABS[0][0]
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
        self.tab = tab if tab in self.views else self.TABS[0][0]
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


class OptionsView(TabsView):
    """Settings, the board, the controller, plugins and the guide on one screen."""

    TABS = (("settings", "Settings", "gear"), ("board", "Board", "cpu"), ("controller", "Control", "joystick"),
            ("plugins", "Plugins", "plug"), ("docs", "Guide", "book-open"))

    def __init__(self, app):
        from gui.views.boards import BoardView
        from gui.views.controller import ControllerView
        from gui.views.docs import DocsView
        from gui.views.plugins import PluginsView
        from gui.views.settings import SettingsView
        super().__init__(app, {"settings": SettingsView(app), "board": BoardView(app),
                               "controller": ControllerView(app), "plugins": PluginsView(app),
                               "docs": DocsView(app)})


class BankScreen(TabsView):
    """The bank, and the GTS that lists its Pokemon online."""

    TABS = (("bank", "Bank", "package"), ("gts", "GTS", "globe"))

    def __init__(self, app):
        from gui.views.bank import BankView
        from gui.views.gts import GtsView
        super().__init__(app, {"bank": BankView(app), "gts": GtsView(app)})
