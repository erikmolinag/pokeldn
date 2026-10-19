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

from gui import language_pack  # noqa: E402
from pokeldn.app.settings import load as load_settings  # noqa: E402
language_pack.use(load_settings().ui_language)   # before any module builds its text

import flet as ft  # noqa: E402

from gui import drop, flet_client, i18n, screen, theme as t  # noqa: E402
from gui.app import App  # noqa: E402
from gui.i18n import tr  # noqa: E402
from gui.localization import flet_locale  # noqa: E402
from gui.views.widgets import page_key  # noqa: E402
from pokeldn import __version__, popup  # noqa: E402
from pokeldn.app import update  # noqa: E402
from pokeldn.app.paths import ROOT  # noqa: E402

# Upstream page names, as other views ask for them, mapped onto poke-app's screens.
ALIASES = {"home": "menu", "board": "options", "settings": "options", "docs": "options", "controller": "options",
           "plugins": "options", "gts": "bank"}
TABS = ("board", "settings", "docs", "controller", "plugins", "gts")   # pages that are a tab of their screen
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
    "bank": ("package", "Bank", "Keep Pokemon on this computer, send them back to a game or trade them on the GTS."),
    "options": ("gear", "Options", "Board, language, keys, plugins and the guide."),
}
FORK = "https://github.com/erikmolinag/pokeldn"
BAR = ft.Colors.with_opacity(0.80, "#FFFFFF")

ANDROID = os.environ.get("POKELDN_PLATFORM") == "android"
IOS = os.environ.get("POKELDN_PLATFORM") == "ios"


def main(page: ft.Page) -> None:
    t.compact = bool(page.width) and page.width < t.COMPACT_WIDTH
    page.title = "pokeldn"
    page.fonts = {t.FONT: "fonts/Nunito.ttf", **t.FONT_ASSETS}
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = page.dark_theme = t.app_theme()
    page.locale_configuration = flet_locale()
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
        from gui.views.screen import BankScreen, OptionsView, ScreenView
        if key == "menu":
            from gui.views.menu import MenuView
            return MenuView(app)
        if key == "options":
            return ScreenView(app, *SCREENS[key], OptionsView(app))
        if key == "bank":
            return ScreenView(app, *SCREENS[key], BankScreen(app))
        from gui.views.games import GamesView
        if key == "trade":
            inner = GamesView(app, single="frlg-trade-host",
                              tools=("frlg-trade-host", "frlg-trade-join", "frlg-trade-online"))
            return ScreenView(app, *SCREENS[key], inner)
        if key == "team":
            from gui.views.home import team_side
            inner = GamesView(app, single="frlg-trade-host", only_offer=True)
            return ScreenView(app, *SCREENS[key], inner, side=None if t.compact else team_side(app))
        if key == "trainer":
            return ScreenView(app, *SCREENS[key], GamesView(app, single="frlg-trainer"))
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
        if t.compact:   # a phone's top bar: the avatar alone
            return ft.Container(avatar, on_click=lambda e: navigate("trainer"), border_radius=19, shadow=t.SHADOW)
        return pill(ft.Row([avatar, body], spacing=10, tight=True), lambda e: navigate("trainer"),
                    padding=ft.Padding(6, 6, 18, 6))

    def render_chrome() -> None:
        key = current["key"]
        c = t.compact
        if c and key == "menu":
            heading.content = ft.Row([ft.Image(src="pokeball.svg", width=28, height=28),
                                      t.text("pokeldn", 20, t.NAVY, weight=ft.FontWeight.W_900)], spacing=10)
        elif c:
            icon, title, detail = SCREENS[key]
            heading.content = ft.Row([
                ft.Container(t.pixel_icon("arrow-left", size=22, color=t.TEXT), width=40, height=40,
                             border_radius=20, bgcolor=t.PANEL, alignment=ft.Alignment.CENTER, shadow=t.SHADOW,
                             border=ft.Border.all(1, t.OUTLINE), on_click=lambda e: back()),
                t.text(tr(title), 18, weight=ft.FontWeight.W_900, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ], spacing=10, expand=True)
        elif key == "menu":
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
        dot = ft.Container(width=10, height=10, border_radius=5, bgcolor=color)
        status.controls = [
            pill(dot if c else ft.Row([dot, t.text(label, 14, t.SOFT, weight=ft.FontWeight.W_800)], spacing=8,
                                      tight=True),
                 lambda e: navigate("options", tab="board"), tr(board.detail),
                 padding=ft.Padding(12, 12, 12, 12) if c else ft.Padding(16, 10, 18, 10)),
            trainer_chip(),
        ]

    def navigate(key: str, **kwargs) -> None:
        if key == "update":
            offer_update(app)
            return
        if key == "games":
            key = TOOL_SCREENS.get(kwargs.get("tool", ""), "trade")
        if key in TABS:
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
    if t.compact:   # a phone: a slim top bar over the screen; no keyboard hints, the fork is in About
        page.add(t.backdrop(ft.Column([
            ft.Container(ft.Row([heading, ft.Container(expand=True), status],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER),
                         height=60, padding=ft.Padding(12, 0, 12, 0), bgcolor=BAR,
                         border=ft.Border(bottom=ft.BorderSide(1, t.OUTLINE))),
            ft.Container(content, expand=True, padding=ft.Padding(10, 10, 10, 6)),
        ], spacing=0, expand=True)))
        navigate("menu")
        compact_start(app)
        return
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
    elif app.plugin_stopped:
        plugin_stopped_notice(app)

    def updated() -> None:
        render_chrome()
        page.update()
    app.update_listeners.append(updated)
    app.plugin_update_listeners.append(updated)
    if getattr(sys, "frozen", False):
        threading.Thread(target=prune_viewers, daemon=True).start()
    # poke-app does not ask Decryptu/pokeldn for app updates: its builds come from the fork's Actions.
    # Installed plugins still ask their own addresses for theirs.
    if app.settings.check_updates:
        app.check_plugin_updates()
    from gui.views.gts import resume
    resume(app)      # a listing or an offer left open is answered while the app runs


def compact_start(app: App) -> None:
    """The phone's start: the same first-run notices, without the desktop's update and viewer housekeeping."""
    if not os.path.isfile(os.path.expanduser(app.settings.keys)):
        welcome(app)
    elif app.plugin_stopped:
        plugin_stopped_notice(app)
    if app.settings.check_updates:
        app.check_plugin_updates()
    from gui.views.gts import resume
    resume(app)


def prune_viewers() -> None:
    try:
        flet_client.prune_cache()
    except Exception:   # housekeeping: a locked or vanished folder waits for the next launch
        pass


def offer_update(app: App) -> None:
    """A newer release on GitHub: installed in place when this copy can replace itself, else its file."""
    release = app.update
    root = update.install_root()
    reason = update.blocker(root) if release.installable else "manual"
    admin = not reason and update.needs_admin(root)

    def close(e):
        app.page.pop_dialog()

    def open_(url):
        def go(e):
            app.page.pop_dialog()
            app.page.run_task(app.open_url, url)
        return go

    def install(e):
        if app.busy:
            note.value, note.color = tr('main.finish_the_running_session_flash_or_cleanup_first_4771cf', 'Finish the running session, flash or cleanup first.'), t.RED
            note.update()
            return
        app.page.pop_dialog()
        install_update(app, release, admin)

    note = t.text(tr('main.you_have_c04a93', 'You have {value0}. ', value0=__version__)
                  + (tr('main.pokeldn_downloads_it_checks_it_and_restarts_in_the_new__d1543b', 'pokeldn downloads it, checks it and restarts in the new version. ') if not reason else
                     tr('main.download_the_new_version_then_replace_this_app_with_it_880281', 'Download the new version, then replace this app with it. ') if release.download != release.page else
                     tr('main.download_the_new_version_for_your_computer_from_the_rel_47361e', 'Download the new version for your computer from the release page, then replace this app with it. '))
                  + (f"{reason} " if reason and reason != "manual" else "")
                  + (tr('main.windows_asks_for_permission_to_change_5b8fb6', 'Windows asks for permission to change {value0}. ', value0=root.parent) if admin else "")
                  + tr('main.your_settings_keys_and_received_pokemon_stay_where_they_d5360a', 'Your settings, keys and received Pokemon stay where they are.'), 13, t.MUTED)
    main = (t.button(tr('main.update_now_63bf04', 'Update now'), install, "download") if not reason else
            t.button(tr('main.download_d6eafe', 'Download'), open_(release.download), "download"))
    app.page.show_dialog(t.dialog(
        semantics_label=tr('main.update_available_ff8b55', 'Update available'),
        title=t.text(tr('main.pokeldn_is_available_005454', 'pokeldn {value0} is available', value0=release.version), 17, weight=ft.FontWeight.W_600),
        content=ft.Container(note, width=460),
        actions=[t.link_button(tr('main.what_s_new_135e91', "What's new"), open_(release.page)),
                 t.secondary_button(tr('main.later_73b6e4', 'Later'), close), main],
    ))
    app.page.update()   # also shown from a background check, where Flet does not flush on its own


def install_update(app: App, release: update.Release, admin: bool = False) -> None:
    """Downloads and checks the release, then quits so the new app can take this one's place."""
    stop = threading.Event()
    status = t.text(tr('main.downloading_f976eb', 'Downloading...'), 13, t.MUTED)
    bar = ft.ProgressBar(value=None, color=t.BLUE, bgcolor=t.FIELD, height=4)
    cancel = t.secondary_button(tr('main.cancel_19766e', 'Cancel'), lambda e: stop.set())
    app.page.show_dialog(t.dialog(
        semantics_label=tr('main.updating_0b5260', 'Updating'), modal=True,
        title=t.text(tr('main.updating_to_47aca3', 'Updating to {value0}', value0=release.version), 17, weight=ft.FontWeight.W_600),
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
            status.value = (tr('main.downloading_of_mb_797da4', 'Downloading {value0:.0f} of {value1:.0f} MB', value0=done / mb, value1=total / mb) if total else
                            tr('main.downloading_mb_3d82fe', 'Downloading {value0:.0f} MB', value0=done / mb))
            bar.value = done / total if total else None
            app.page.update()
        app.ui(show)

    def failed(message: str) -> None:
        app.page.pop_dialog()
        app.page.show_dialog(t.dialog(
            semantics_label=tr('main.update_failed_e58282', 'Update failed'),
            title=t.text(tr('main.the_update_did_not_install_d79712', 'The update did not install'), 17, weight=ft.FontWeight.W_600),
            content=ft.Container(t.text(tr('main.this_app_is_unchanged_you_can_download_the_new_version__8f43d1', '{value0}{value1}. This app is unchanged; you can download the new version yourself.', value0=message[:1].upper(), value1=message[1:]), 13, t.MUTED), width=460),
            actions=[t.secondary_button(tr('main.close_7d9eb7', 'Close'), lambda e: app.page.pop_dialog()),
                     t.button(tr('main.download_d6eafe', 'Download'), lambda e: (app.page.pop_dialog(),
                                                     app.page.run_task(app.open_url, release.download)), "download")]))
        app.page.update()

    def restart() -> None:
        status.value, bar.value, cancel.disabled = tr('main.restarting_in_the_new_version_d1dfd3', 'Restarting in the new version...'), None, True
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
            update.start_swap(new, root, release.version, admin=admin)
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
        app.page.show_dialog(ft.SnackBar(ft.Text(tr('main.pokeldn_updated_to_1f62a1', 'pokeldn updated to {value0}', value0=__version__)), duration=4000))
        return
    popup.acknowledge(tr('main.the_update_did_not_install_d79712', 'The update did not install'),
                      tr('main.pokeldn_could_not_replace_this_app_this_app_is_unchange_23fff0', 'pokeldn {value0} could not replace this app: {value1}. This app is unchanged.', value0=version, value1=error or tr('main.it_opened_the_old_version_6f6d59', 'it opened the old version')), id="update-failed", label=tr('main.close_7d9eb7', 'Close'), tone="error")


def plugin_stopped_notice(app: App) -> None:
    """A plugin froze or closed the app last time while it started; App turned it off."""
    popup.confirm(tr('main.a_plugin_was_turned_off_ed25fc', 'A plugin was turned off'),
                  tr('main.pokeldn_closed_or_stopped_answering_last_time_while_sta_bc8a75', 'pokeldn closed or stopped answering last time while starting the plugin {value0}. It is off now; turn it on again on the Plugins page once its author has a fix.', value0=app.plugin_stopped),
                  tr('main.open_plugins_2faa63', 'Open Plugins'), tr('main.not_now_a0e63d', 'Not now'), id="plugin-stopped", tone="warning",
                  on_agree=lambda: app.ui(lambda: app.navigate("plugins")))


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
            tr("Plug your ESP32 into the phone with a USB data cable.") if ANDROID else
            tr("Plug in your ESP32 with a USB data cable."),
            tr("Read your trainer from the console, so the Pokemon built here are yours."),
        ]),
        ft.Row([t.link_button(tr("Read the setup guide"), instructions)]),
    ], spacing=8, tight=True)
    note = t.text(tr('main.drop_prod_keys_here_or_add_keys_later_in_settings_b49b46', 'Drop prod.keys here, or add keys later in Settings.') if drop.AVAILABLE else
                  tr('main.add_keys_later_in_settings_8bc2f9', 'Add keys later in Settings.'), 12, t.FAINT, expand=not t.compact)
    buttons = [t.secondary_button(tr('main.later_73b6e4', 'Later'), close),
               t.button(tr('main.choose_prod_keys_782614', 'Choose prod.keys'), choose, "key")]
    footer = (ft.Column([note, ft.Row(buttons, spacing=8, alignment=ft.MainAxisAlignment.END)], spacing=10) if t.compact
              else ft.Row([note, *buttons], spacing=8))
    app.page.show_dialog(t.dialog(
        modal=True, content_padding=0, actions_padding=0, inset_padding=14 if t.compact else 32,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        semantics_label=tr('main.welcome_to_pokeldn_319d9e', 'Welcome to pokeldn'),
        content=drop.target(ft.Container(ft.Column([
            ft.Container(body, padding=ft.Padding(28, 22, 18, 8)),
            ft.Container(footer, padding=ft.Padding(28, 12, 24, 24)),
        ], spacing=0, tight=True), width=500, border_radius=20), dropped),
    ))


def window_header(page: ft.Page) -> ft.Control:
    mac = sys.platform == "darwin"
    title = ft.Container(height=40)
    drag = title if page.web else ft.WindowDragArea(title)
    drag.expand = True
    controls = [drag]
    if not page.web and not mac:
        async def close(e):
            await page.window.close()

        def minimize(e):
            page.window.minimized = True
            page.update()

        def maximize(e):
            page.window.maximized = not page.window.maximized
            page.update()

        controls.extend([
            ft.IconButton(ft.Icons.REMOVE, tooltip=tr('main.minimize_d72e31', 'Minimize'), on_click=minimize, icon_size=16),
            ft.IconButton(ft.Icons.CROP_SQUARE, tooltip=tr('main.maximize_or_restore_9e47a6', 'Maximize or restore'), on_click=maximize, icon_size=14),
            ft.IconButton(ft.Icons.CLOSE, tooltip=tr('main.close_7d9eb7', 'Close'), on_click=close, icon_size=16),
        ])
    return ft.Container(ft.Row(controls, spacing=0), height=40)


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
