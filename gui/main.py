import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokeldn.app import paths  # noqa: E402,F401  (puts the repository and vendor/LDN on sys.path)

if len(sys.argv) > 2 and sys.argv[1] in ("--run", "--module"):
    from pokeldn.app.runner import child
    child(sys.argv[1:])
    sys.exit(0)

# The app's own process never drives a board: an inherited POKELDN_RADIO would open the port as
# soon as pokeldn.ldn is imported.
os.environ.pop("POKELDN_RADIO", None)

import flet as ft  # noqa: E402

from gui import drop, flet_client, i18n, screen, theme as t  # noqa: E402
from gui.app import App  # noqa: E402
from gui.i18n import tr  # noqa: E402
from gui.views.widgets import page_key  # noqa: E402
from pokeldn import __version__  # noqa: E402
from pokeldn.app.paths import ROOT  # noqa: E402

# Upstream page names, as other views ask for them, mapped onto poke-app's screens.
ALIASES = {"home": "menu", "board": "options", "settings": "options", "docs": "options"}
TOOL_SCREENS = {"frlg-trainer": "trainer", "frlg-trade-host": "trade", "frlg-trade-join": "trade",
                "frlg-gift": "gift"}
# screen key -> (icon, title, detail), the header each screen shows
SCREENS = {
    "trade": ("arrows-horizontal", "TRADE", "Send a Pokemon built for your save, or receive one."),
    "gift": ("gift", "MYSTERY GIFT", "Items, eggs, event Pokemon and game boosts."),
    "team": ("pokeball", "POKEMON", "Build the Pokemon you will trade: they belong to your trainer."),
    "trainer": ("trainer", "MY TRAINER", "Read your name, Trainer ID and Secret ID from the console."),
    "save": ("save", "MY SAVE", "Copy your whole save to this computer, or put one back."),
    "options": ("gear", "OPTIONS", "Board, language, keys and the guide."),
}


def main(page: ft.Page) -> None:
    page.title = "pokeldn"
    page.fonts = {t.FONT: "fonts/Rubik.ttf"}
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = page.dark_theme = t.app_theme()
    page.bgcolor = t.BG
    page.padding = 0
    # 1440 x 900 overflows a 13-inch MacBook Air (1440 x 932 points less the menu bar): fit, then center.
    (width, height), (min_width, min_height) = screen.fit((1440, 900), (1180, 720), screen.size())
    page.window.min_width, page.window.min_height = min_width, min_height
    page.window.width, page.window.height = width, height
    page.window.bgcolor = t.BG

    app = App(page)
    i18n.set_language(app.settings.ui_language)
    views: dict[str, object] = {}
    content = ft.Container(expand=True)
    hints = ft.Row(spacing=30, alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    status = ft.Row(spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    current = {"key": "menu"}

    def build(key: str):
        from gui.views.screen import OptionsView, ScreenView
        if key == "menu":
            from gui.views.menu import MenuView
            return MenuView(app)
        if key == "options":
            return ScreenView(app, *SCREENS[key], OptionsView(app))
        from gui.views.games import GamesView
        if key == "trade":
            inner = GamesView(app, single="frlg-trade-host", tools=("frlg-trade-host", "frlg-trade-join"))
            return ScreenView(app, *SCREENS[key], inner)
        if key == "team":
            from gui.views.home import team_side
            inner = GamesView(app, single="frlg-trade-host", only_offer=True)
            return ScreenView(app, *SCREENS[key], inner, side=team_side(app))
        if key == "trainer":
            return ScreenView(app, *SCREENS[key], GamesView(app, single="frlg-trainer"))
        if key == "save":
            return ScreenView(app, *SCREENS[key], GamesView(app, single="frlg-gift"), {"gift_mode": "save"})
        return ScreenView(app, *SCREENS["gift"], GamesView(app, single="frlg-gift"), {"gift_mode": "gift"})

    def hint(letter: str, label: str) -> ft.Control:
        from gui.views.screen import key_chip
        return ft.Row([key_chip(letter), t.text(tr(label), 17, weight=ft.FontWeight.W_800)], spacing=10, tight=True)

    def render_chrome() -> None:
        on_menu = current["key"] == "menu"
        hints.controls = ([hint("↕", "Move"), hint("A", "Choose")] if on_menu else
                          [hint("B", "Back")])
        board = app.board_status()
        mine = app.settings.my_trainer
        game = {"firered": "FireRed", "leafgreen": "LeafGreen"}.get(mine.get("version") or "", "FireRed & LeafGreen")
        status.controls = [
            ft.Container(width=14, height=14, border_radius=7,
                         bgcolor=t.GREEN if board.ready else t.AMBER if board.state != "checking" else t.INFO,
                         tooltip=tr(board.title)),
            t.text(f"POKELDN · {tr(game).upper()}", 21, weight=ft.FontWeight.W_900),
        ]

    def navigate(key: str, **kwargs) -> None:
        if key == "update":
            offer_update(app)
            return
        if key == "games":
            key = TOOL_SCREENS.get(kwargs.get("tool", ""), "trade")
        if key in ("board", "settings", "docs"):
            kwargs.setdefault("tab", key)
        key = ALIASES.get(key, key)
        previous = views.get(current["key"])
        if previous is not None and hasattr(previous, "leave"):
            previous.leave()
        current["key"] = key
        if key not in views:
            views[key] = build(key)
        view = views[key]
        if hasattr(view, "enter"):
            view.enter(**kwargs)
        content.content = view.control
        render_chrome()
        page.update()

    def back() -> None:
        if current["key"] != "menu":
            navigate("menu")

    def relocalize() -> None:
        """The interface language changed: build every page again in it."""
        i18n.set_language(app.settings.ui_language)
        previous = views.get(current["key"])
        if previous is not None and hasattr(previous, "leave"):
            previous.leave()
        views.clear()
        app.board_listeners.clear()
        app.trainer_listeners.clear()
        app.board_listeners.append(chrome_changed)
        app.trainer_listeners.append(chrome_changed)
        navigate(current["key"])

    def chrome_changed() -> None:
        render_chrome()
        page.update()

    def keyboard(e) -> None:
        """Esc goes back like B; on the menu, arrows and Enter drive it like a controller."""
        page_key(e)
        if e.key == "Escape":
            back()
            return
        view = views.get(current["key"])
        if current["key"] == "menu" and view is not None:
            view.key(e.key)

    app.navigate = navigate
    app.back = back
    app.relocalize = relocalize
    app.board_listeners.append(chrome_changed)
    app.trainer_listeners.append(chrome_changed)
    page.on_keyboard_event = keyboard     # set once, before a code box takes the focus
    page.add(t.backdrop(ft.Stack([
        ft.Container(status, left=48, top=26),
        ft.Container(content, left=40, right=40, top=76, bottom=78),
        ft.Container(ft.Container(hints, padding=ft.Padding(48, 0, 48, 0)), left=0, right=0, bottom=0, height=62,
                     bgcolor=ft.Colors.with_opacity(0.62, "#0B0420")),
    ], expand=True)))
    navigate("menu")
    if not page.web:
        page.run_task(page.window.center)
    if not os.path.isfile(os.path.expanduser(app.settings.keys)):
        welcome(app)

    def updated() -> None:
        render_chrome()
        page.update()
    app.update_listeners.append(updated)
    if getattr(sys, "frozen", False):
        threading.Thread(target=prune_viewers, daemon=True).start()
    # poke-app does not ask Decryptu/pokeldn for updates: a release there is the upstream app, not this one.


def prune_viewers() -> None:
    try:
        flet_client.prune_cache()
    except Exception:   # housekeeping: a locked or vanished folder waits for the next launch
        pass


def offer_update(app: App) -> None:
    """A newer release on GitHub: its file for this computer, and its notes."""
    release = app.update

    def close(e):
        app.page.pop_dialog()

    def open_(url):
        def go(e):
            app.page.pop_dialog()
            app.page.run_task(app.open_url, url)
        return go

    direct = release.download != release.page
    app.page.show_dialog(t.dialog(
        semantics_label="Update available",
        title=t.text(f"pokeldn {release.version} is available", 17, weight=ft.FontWeight.W_600),
        content=ft.Container(t.text(
            f"You have {__version__}. "
            + ("Download the new version, then replace this app with it. " if direct else
               "Download the new version for your computer from the release page, then replace this app "
               "with it. ")
            + "Your settings, keys and received Pokemon stay where they are.", 13, t.MUTED), width=460),
        actions=[t.link_button("What's new", open_(release.page)),
                 t.secondary_button("Later", close),
                 t.button("Download", open_(release.download), "download")],
    ))
    app.page.update()   # also shown from a background check, where Flet does not flush on its own


def welcome(app: App) -> None:
    """The one file the app cannot ship: the user's own Switch keys."""
    def close(e):
        app.page.pop_dialog()

    def use(path: str) -> None:
        app.settings.keys = path
        app.settings.save()
        app.page.pop_dialog()
        app.navigate("home")

    async def choose(e):
        files = await app.picker.pick_files(allowed_extensions=["keys"], file_type=ft.FilePickerFileType.CUSTOM)
        if files and files[0].path:
            use(files[0].path)

    def dropped(paths: list[str]) -> None:
        if path := next((p for p in paths if drop.suffix(p) == "keys"), ""):
            use(path)

    def instructions(e):
        app.page.pop_dialog()
        app.navigate("docs", doc="guide")

    body = ft.Column([
        ft.Row([ft.Image(src="pokeball.svg", width=40, height=40), ft.Container(expand=True),
                t.icon_button("close", close, tr("Close welcome"))],
               vertical_alignment=ft.CrossAxisAlignment.START),
        t.text(tr("Welcome to pokeldn"), 26, weight=ft.FontWeight.W_900),
        t.text(tr("Trade and send gifts over local wireless, right from your computer."), 14, t.MUTED),
        ft.Container(height=6),
        t.step_list([
            tr("Choose prod.keys dumped from your own console. The keys decrypt local wireless messages and "
               "stay on this computer."),
            tr("Plug in your ESP32 with a USB data cable."),
            tr("Read your trainer from the console, so the Pokemon built here are yours."),
        ]),
        ft.Row([t.link_button(tr("Read the setup guide"), instructions)]),
    ], spacing=8, tight=True)
    app.page.show_dialog(t.dialog(
        modal=True, content_padding=0, actions_padding=0, inset_padding=32,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        semantics_label=tr("Welcome to pokeldn"),
        content=drop.target(ft.Container(ft.Column([
            ft.Container(body, padding=ft.Padding(28, 22, 18, 8)),
            ft.Container(ft.Row([
                t.text(tr("Drop prod.keys here, or add keys later in Settings.") if drop.AVAILABLE else
                       tr("Add keys later in Settings."), 12, t.FAINT, expand=True),
                t.secondary_button(tr("Later"), close),
                t.button(tr("Choose prod.keys"), choose, "key"),
            ], spacing=8), padding=ft.Padding(28, 12, 24, 24)),
        ], spacing=0, tight=True), width=520, border_radius=26), dropped),
    ))


def run() -> None:
    assets = os.path.join(ROOT, "gui", "assets")
    drop.use_client()
    if os.environ.get("POKELDN_GUI_WEB"):   # a browser preview, for screenshots
        ft.run(main, assets_dir=assets, view=ft.AppView.WEB_BROWSER, no_cdn=True,
               port=int(os.environ["POKELDN_GUI_WEB"]))
    else:
        ft.run(main, assets_dir=assets)


if __name__ == "__main__":
    run()
