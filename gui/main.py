import os
import subprocess
import sys
import tarfile
import threading
import time
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokeldn.app import paths  # noqa: E402,F401  (puts the repository and vendor/LDN on sys.path)

if len(sys.argv) > 2 and sys.argv[1] in ("--run", "--module"):
    from pokeldn.app.runner import child
    child(sys.argv[1:])
    sys.exit(0)

if len(sys.argv) == 6 and sys.argv[1] == "--apply-update":
    # The new app, unpacked by the old one, replaces it; pokeldn.app.update.start_swap passes these.
    from pathlib import Path
    from gui.updating import run
    new, target, pid, version = sys.argv[2:]
    os.chdir(Path(new).parent)   # an older app started this helper in target; Windows then refuses the rename
    sys.exit(run(Path(new), Path(target), int(pid), version))

# The app's own process never drives a board: an inherited POKELDN_RADIO would open the port as
# soon as pokeldn.ldn is imported.
os.environ.pop("POKELDN_RADIO", None)

import flet as ft  # noqa: E402

from gui import drop, flet_client, i18n, screen, theme as t  # noqa: E402
from gui.app import App  # noqa: E402
from gui.i18n import tr  # noqa: E402
from gui.views.widgets import page_key  # noqa: E402
from pokeldn import __version__  # noqa: E402
from pokeldn.app import update  # noqa: E402
from pokeldn.app.paths import ROOT  # noqa: E402

# Upstream page names, as other views ask for them, mapped onto poke-app's screens.
ALIASES = {"home": "menu", "board": "options", "settings": "options", "docs": "options", "controller": "options"}
TOOL_SCREENS = {"frlg-trainer": "trainer", "frlg-trade-host": "trade", "frlg-trade-join": "trade",
                "frlg-trade-online": "trade",
                "frlg-gift": "gift"}
# screen key -> (icon, title, detail), what the top bar shows on each screen
SCREENS = {
    "trade": ("arrows-horizontal", "Trade", "Send a Pokemon built for your save, or receive one."),
    "gift": ("gift", "Mystery Gift", "Items, eggs, event Pokemon and game boosts."),
    "team": ("pokeball", "Pokemon", "Build the Pokemon you will trade: they belong to your trainer."),
    "trainer": ("trainer", "My trainer", "Read your name, Trainer ID and Secret ID from the console."),
    "save": ("save", "My save", "Copy your whole save to this computer, or put one back."),
    "bank": ("package", "Bank", "Keep Pokemon on this computer and send them back to a game."),
    "options": ("gear", "Options", "Board, language, keys and the guide."),
}
FORK = "https://github.com/erikmolinag/pokeldn"
BAR = ft.Colors.with_opacity(0.80, "#FFFFFF")


def main(page: ft.Page) -> None:
    page.title = "pokeldn"
    page.fonts = {t.FONT: "fonts/Nunito.ttf"}
    page.theme_mode = ft.ThemeMode.LIGHT
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
    hints = ft.Row(spacing=24, alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    heading = ft.Container()
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
            inner = GamesView(app, single="frlg-trade-host",
                              tools=("frlg-trade-host", "frlg-trade-join", "frlg-trade-online"))
            return ScreenView(app, *SCREENS[key], inner)
        if key == "team":
            from gui.views.home import team_side
            inner = GamesView(app, single="frlg-trade-host", only_offer=True)
            return ScreenView(app, *SCREENS[key], inner, side=team_side(app))
        if key == "trainer":
            return ScreenView(app, *SCREENS[key], GamesView(app, single="frlg-trainer"))
        if key == "bank":
            from gui.views.bank import BankView
            return ScreenView(app, *SCREENS[key], BankView(app))
        if key == "save":
            return ScreenView(app, *SCREENS[key], GamesView(app, single="frlg-gift"), {"gift_mode": "save"})
        return ScreenView(app, *SCREENS["gift"], GamesView(app, single="frlg-gift"), {"gift_mode": "gift"})

    def hint(letter: str, label: str) -> ft.Control:
        from gui.views.screen import key_chip
        return ft.Row([key_chip(letter), t.text(tr(label), 14, t.SOFT, weight=ft.FontWeight.W_800)], spacing=8,
                      tight=True)

    def pill(content: ft.Control, on_click, tooltip: str = "", padding=ft.Padding(16, 10, 18, 10)) -> ft.Control:
        return ft.Container(content, padding=padding, border_radius=999, bgcolor=t.PANEL,
                            border=ft.Border.all(1, t.OUTLINE), shadow=t.SHADOW, on_click=on_click,
                            tooltip=tooltip or None)

    def trainer_chip() -> ft.Control:
        from gui.views.trainer import BOY, GIRL
        mine = app.settings.my_trainer
        if mine.get("name"):
            gender = int(mine.get("gender") or 0)
            face = t.text(mine["name"][:1].upper(), 17, t.INK, weight=ft.FontWeight.W_900)
            body = ft.Column([t.text(mine["name"], 15, weight=ft.FontWeight.W_900),
                              t.text(f"{tr('Trainer ID')} {int(mine['tid']):05d}", 11, t.MUTED,
                                     weight=ft.FontWeight.W_800)], spacing=0, tight=True)
            color = GIRL if gender else BOY
        else:
            face, color = t.pixel_icon("trainer", size=20, color=t.INK), t.FAINT
            body = t.text(tr("Read now"), 14, weight=ft.FontWeight.W_800)
        avatar = ft.Container(face, width=38, height=38, border_radius=19, bgcolor=color,
                              alignment=ft.Alignment.CENTER)
        return pill(ft.Row([avatar, body], spacing=10, tight=True), lambda e: navigate("trainer"),
                    padding=ft.Padding(6, 6, 18, 6))

    def render_chrome() -> None:
        key = current["key"]
        if key == "menu":
            heading.content = ft.Row([
                ft.Container(ft.Image(src="pokeball.svg", width=32, height=32), width=50, height=50,
                             border_radius=25, bgcolor=t.PANEL, alignment=ft.Alignment.CENTER, shadow=t.SHADOW),
                ft.Column([t.text("pokeldn", 26, t.NAVY, weight=ft.FontWeight.W_900),
                           t.text(tr("FireRed & LeafGreen"), 12, t.MUTED, weight=ft.FontWeight.W_800)],
                          spacing=0, tight=True),
            ], spacing=14)
            hints.controls = [hint("↕", "Move"), hint("A", "Choose")]
        else:
            icon, title, detail = SCREENS[key]
            heading.content = ft.Row([
                ft.Container(t.pixel_icon("arrow-left", size=24, color=t.TEXT), width=48, height=48,
                             border_radius=24, bgcolor=t.PANEL, alignment=ft.Alignment.CENTER, shadow=t.SHADOW,
                             border=ft.Border.all(1, t.OUTLINE), on_click=lambda e: back(),
                             tooltip=tr("Back to the menu (Esc)")),
                t.badge_icon(icon, 48, 24),
                ft.Column([t.text(tr(title), 24, weight=ft.FontWeight.W_900),
                           t.text(tr(detail), 13, t.MUTED, weight=ft.FontWeight.W_700)], spacing=0, tight=True),
            ], spacing=14)
            hints.controls = [hint("B", "Back")]
        board = app.board_status()
        color = t.GREEN if board.ready else t.INFO if board.state == "checking" else t.AMBER
        label = tr("Board ready on {port}", port=board.port) if board.ready else tr(board.title)
        status.controls = [
            pill(ft.Row([ft.Container(width=10, height=10, border_radius=5, bgcolor=color),
                         t.text(label, 14, t.SOFT, weight=ft.FontWeight.W_800)], spacing=8, tight=True),
                 lambda e: navigate("options", tab="board"), tr(board.detail)),
            trainer_chip(),
        ]

    def navigate(key: str, **kwargs) -> None:
        if key == "update":
            offer_update(app)
            return
        if key == "games":
            key = TOOL_SCREENS.get(kwargs.get("tool", ""), "trade")
        if key in ("board", "settings", "docs", "controller"):
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
    fork = ft.Container(ft.Row([
        t.pixel_icon("fork", size=16, color=t.MUTED),
        t.text(tr("pokeldn · a fork by {name}", name="erks"), 13, t.MUTED, weight=ft.FontWeight.W_800),
        t.text("github.com/erikmolinag/pokeldn", 13, t.ACCENT, weight=ft.FontWeight.W_800),
    ], spacing=8, tight=True), on_click=lambda e: page.run_task(app.open_url, FORK), tooltip=FORK)
    page.add(t.backdrop(ft.Column([
        ft.Container(ft.Row([heading, ft.Container(expand=True), status],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER),
                     height=84, padding=ft.Padding(32, 0, 32, 0), bgcolor=BAR,
                     border=ft.Border(bottom=ft.BorderSide(1, t.OUTLINE))),
        ft.Container(content, expand=True, padding=ft.Padding(32, 26, 32, 24)),
        ft.Container(ft.Row([fork, ft.Container(expand=True), hints],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER),
                     height=54, padding=ft.Padding(32, 0, 32, 0), bgcolor=BAR,
                     border=ft.Border(top=ft.BorderSide(1, t.OUTLINE))),
    ], spacing=0, expand=True)))
    navigate("menu")
    if not page.web:
        page.run_task(page.window.center)
    outcome = update.finish(update.install_root())
    if not os.path.isfile(os.path.expanduser(app.settings.keys)):
        welcome(app)
    elif outcome:
        updated_notice(app, outcome)

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
    """A newer release on GitHub: installed in place when this copy can replace itself, else its file."""
    release = app.update
    reason = update.blocker(update.install_root()) if release.installable else "manual"

    def close(e):
        app.page.pop_dialog()

    def open_(url):
        def go(e):
            app.page.pop_dialog()
            app.page.run_task(app.open_url, url)
        return go

    def install(e):
        if app.busy:
            note.value, note.color = "Finish the running session, flash or cleanup first.", t.RED
            note.update()
            return
        app.page.pop_dialog()
        install_update(app, release)

    note = t.text(f"You have {__version__}. "
                  + ("pokeldn downloads it, checks it and restarts in the new version. " if not reason else
                     "Download the new version, then replace this app with it. " if release.download != release.page else
                     "Download the new version for your computer from the release page, then replace this app "
                     "with it. ")
                  + (f"{reason} " if reason and reason != "manual" else "")
                  + "Your settings, keys and received Pokemon stay where they are.", 13, t.MUTED)
    main = (t.button("Update now", install, "download") if not reason else
            t.button("Download", open_(release.download), "download"))
    app.page.show_dialog(t.dialog(
        semantics_label="Update available",
        title=t.text(f"pokeldn {release.version} is available", 17, weight=ft.FontWeight.W_600),
        content=ft.Container(note, width=460),
        actions=[t.link_button("What's new", open_(release.page)),
                 t.secondary_button("Later", close), main],
    ))
    app.page.update()   # also shown from a background check, where Flet does not flush on its own


def install_update(app: App, release: update.Release) -> None:
    """Downloads and checks the release, then quits so the new app can take this one's place."""
    stop = threading.Event()
    status = t.text("Downloading...", 13, t.MUTED)
    bar = ft.ProgressBar(value=None, color=t.BLUE, bgcolor=t.FIELD, height=4)
    cancel = t.secondary_button("Cancel", lambda e: stop.set())
    app.page.show_dialog(t.dialog(
        semantics_label="Updating", modal=True,
        title=t.text(f"Updating to {release.version}", 17, weight=ft.FontWeight.W_600),
        content=ft.Container(ft.Column([status, bar], spacing=12, tight=True), width=460),
        actions=[cancel]))
    app.page.update()
    shown = [0.0]

    def progress(done: int, total: int) -> None:
        now = time.monotonic()
        if now - shown[0] < 0.2 and done != total:
            return
        shown[0] = now

        def show():
            mb = 1 << 20
            status.value = (f"Downloading {done / mb:.0f} of {total / mb:.0f} MB" if total else
                            f"Downloading {done / mb:.0f} MB")
            bar.value = done / total if total else None
            app.page.update()
        app.ui(show)

    def failed(message: str) -> None:
        app.page.pop_dialog()
        app.page.show_dialog(t.dialog(
            semantics_label="Update failed",
            title=t.text("The update did not install", 17, weight=ft.FontWeight.W_600),
            content=ft.Container(t.text(f"{message[:1].upper()}{message[1:]}. This app is unchanged; "
                                        "you can download the new version yourself.", 13, t.MUTED), width=460),
            actions=[t.secondary_button("Close", lambda e: app.page.pop_dialog()),
                     t.button("Download", lambda e: (app.page.pop_dialog(),
                                                     app.page.run_task(app.open_url, release.download)), "download")]))
        app.page.update()

    def restart() -> None:
        status.value, bar.value, cancel.disabled = "Restarting in the new version...", None, True
        app.page.update()

        async def quit_():
            await app.page.window.destroy()
        app.page.run_task(quit_)
        # The helper waits for this process to end; a window that never closes must not hold it.
        threading.Timer(5.0, lambda: os._exit(0)).start()

    def work():
        root = update.install_root()
        try:
            new = update.prepare(release, progress, stop.is_set)
            if stop.is_set():
                raise update.Cancelled
            update.start_swap(new, root, release.version)
            # This window stays until the helper's own is up, so one is always on screen.
            update.wait_for(update.READY.exists, 15.0)
        except update.Cancelled:
            app.ui(app.page.pop_dialog)
            return
        except (OSError, subprocess.CalledProcessError, tarfile.TarError, zipfile.BadZipFile) as error:
            message = str(error) or type(error).__name__
            app.ui(lambda: failed(message))
            return
        app.ui(restart)

    threading.Thread(target=work, daemon=True).start()


def updated_notice(app: App, outcome: dict) -> None:
    """What the last update did, shown once by the app it opened."""
    error, version = outcome.get("error") or "", str(outcome.get("version") or "")
    if not error and version == __version__:
        app.page.show_dialog(ft.SnackBar(ft.Text(f"pokeldn updated to {__version__}"), duration=4000))
        return
    app.page.show_dialog(t.dialog(
        semantics_label="Update failed",
        title=t.text("The update did not install", 17, weight=ft.FontWeight.W_600),
        content=ft.Container(t.text(f"pokeldn {version} could not replace this app: "
                                    f"{error or 'it opened the old version'}. This app is unchanged.",
                                    13, t.MUTED), width=460),
        actions=[t.button("Close", lambda e: app.page.pop_dialog())]))


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
