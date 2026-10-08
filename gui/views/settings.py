import copy
import os
import threading

import flet as ft

from gui import i18n, theme as t
from gui.app import keys_found
from gui.i18n import tr
from pokeldn import __version__
from pokeldn.app.paths import SESSION
from pokeldn.app.sprites import CACHE
from pokeldn.app.settings import LANGUAGES
from pokeldn.app import storage
from gui.views.widgets import PathField, open_folder

LINKS = (("Docs", "https://decryptu.github.io/pokeldn/"),
         ("GitHub", "https://github.com/Decryptu/pokeldn"),
         ("Discord", "https://discord.gg/PyvaVYnpXC"))


class SettingsView:
    def __init__(self, app):
        self.app = app
        self.keys_state = ft.Container()
        self.sprite_state = t.text("", 12, t.MUTED)
        self.update_state = t.text("", 12, t.MUTED)
        self.storage_state = t.text(tr("Checking local files..."), 12, t.MUTED)
        self.storage_result = t.text("", 12, t.MUTED, visible=False)
        self.storage_inventory = storage.Inventory()
        self.storage_work = False
        self.clear_button = t.button(tr("Clear local files"), self._clear_local, "folder", filled=False,
                                     disabled=True)
        self.shown = self.asked = False
        app.update_listeners.append(self._update_shown)
        self._update_text()
        self.show_advanced = False
        self.column = ft.Column(spacing=t.GAP, width=760)
        self.scroll = ft.ListView([ft.Row([self.column], alignment=ft.MainAxisAlignment.CENTER)],
                                  padding=ft.Padding(4, 8, 4, 24), expand=True)
        self.control = t.fade(self.scroll)
        self.render()

    def enter(self, **_) -> None:
        self.shown = True
        self._storage_refresh()

    def leave(self) -> None:
        self.shown = False

    def save(self, name: str, value) -> None:
        setattr(self.app.settings, name, value)
        self.app.settings.save()

    def render(self) -> None:
        s = self.app.settings
        home = lambda: os.path.expanduser("~")   # noqa: E731
        keys = PathField(self.app.picker, home, s.keys, "file", ("keys",), self._keys)
        received = PathField(self.app.picker, home, s.received, "dir", on_change=lambda v: self.save("received", v))
        self._keys(s.keys, update=False)
        speed = t.dropdown([("921600", tr("921600 (default)")), ("1500000", tr("1500000 (faster, needs a good cable)"))],
                           str(s.baud), on_select=lambda e: self.save("baud", int(e.control.value)))

        def number(name, label, valid, size):
            def store(e):
                try:
                    value = int(e.control.value)
                except ValueError:
                    return
                if valid(value):
                    self.save(name, value)
            return ft.Column([t.text(label, 11, t.MUTED),
                              t.field(value=str(getattr(s, name)), mono=True, digits=True, limit=size,
                                      on_change=store)],
                             spacing=4, expand=True)

        gba = lambda v: 0 <= v <= 65535   # noqa: E731
        # pokeldn's own identity on the link (the partner the console sees), kept off the player's trainer.
        trainer = ft.Column([
            ft.Row([
                ft.Column([t.text(tr("Name"), 11, t.MUTED),
                           t.field(value=s.ot, limit=7, on_change=lambda e: self.save("ot", e.control.value[:7]))],
                          spacing=4, expand=True),
                ft.Column([t.text(tr("Language"), 11, t.MUTED),
                           t.dropdown([(k, tr(v)) for k, v in LANGUAGES if k != "8"], str(s.language),
                                      on_select=lambda e: self.save("language", int(e.control.value)))],
                          spacing=4, expand=True),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([
                number("tid", tr("Trainer ID"), gba, 5),
                number("sid", tr("Secret ID"), gba, 5),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START),
        ], spacing=10)
        mine = self._my_trainer_editor()
        language = t.dropdown([(code, name) for code, name in i18n.LANGUAGES], s.ui_language,
                              on_select=self._language)

        def switch(name, label, help_):
            return t.card(label, None, help_,
                          trailing=t.switch(getattr(s, name), lambda e: self.save(name, e.control.value)))

        def link(label, url):
            return t.link_button(tr(label), lambda e: self.app.page.run_task(self.app.open_url, url))

        def section(label):
            return ft.Container(t.text(tr(label), 12, t.MUTED, weight=ft.FontWeight.W_800),
                                padding=ft.Padding(4, 8, 0, 0))

        advanced = [
            t.card(tr("pokeldn's trainer on the link"), trainer,
                   tr("The partner your console sees during a trade or a gift. It is not your trainer: the "
                      "Pokemon you build carry the trainer card above.")),
            t.card(tr("Serial speed"), speed, tr("How fast the computer talks to the board. Keep the default "
                                                 "unless a guide says otherwise.")),
            switch("board_trace", tr("Record the board's serial traffic"),
                   tr("Adds the board's counters and every serial message to the session record. Only for radio "
                      "problems someone asked you to report.")),
            t.card(tr("Pokemon sprites"), ft.Row([t.button(tr("Clear the cache"), self._clear_sprites, "refresh",
                                                            filled=False), self.sprite_state], spacing=10),
                   tr("Sprites come from PokeAPI and are kept on this computer after the first download. The app "
                      "works without them."),
                   trailing=t.switch(s.sprites, lambda e: self.save("sprites", e.control.value))),
        ]
        self.column.controls = [   # the Options screen's header names the page
            section("The app"),
            t.card(tr("Language of the app"), ft.Row([ft.Container(language, width=260)]),
                   tr("The language of every screen. Pokemon, moves and items keep your game's names.")),
            section("Your trainer"),
            t.card(tr("Your trainer card"), mine,
                   tr("The original trainer of every Pokemon you build: read it from your console, or type it as "
                      "your game's trainer card shows it.")),
            section("Your setup"),
            t.card(tr("Switch keys"), ft.Column([keys.control, self.keys_state], spacing=8),
                   tr("prod.keys dumped from your own console. Needed to talk to the games; it never leaves this "
                      "computer.")),
            t.card(tr("Received Pokemon"), ft.Row([ft.Container(received.control, expand=True),
                                                   t.icon_button("external-link",
                                                                 lambda e: open_folder(os.path.expanduser(s.received)),
                                                                 tr("Open it"))]),
                   tr("Where the Pokemon a console sends you are saved.")),
            section("Storage"),
            t.card(tr("Local files"), ft.Column([
                self.storage_state,
                ft.Row([self.clear_button], spacing=10),
                self.storage_result,
            ], spacing=8),
                   tr("Free space used by session records, logs, temporary offers and unused built Pokemon. "
                      "Your received Pokemon, selected offers, keys, firmware and settings are kept.")),
            section("Bug reports"),
            t.card(tr("Record every session"), ft.Row([t.button(tr("Open the records"), lambda e: open_folder(
                str(SESSION / "captures")), "folder", filled=False)]),
                   tr("Keeps a small record of each session. When something fails, attach the latest file to "
                      "your report."),
                   trailing=t.switch(s.capture, lambda e: self.save("capture", e.control.value))),
            ft.Row([t.link_button(tr("Hide advanced settings") if self.show_advanced else
                                  tr("Show advanced settings"), self._toggle_advanced)]),
            *(advanced if self.show_advanced else []),
            t.card(tr("About this app"), ft.Row([link(label, url) for label, url in LINKS], spacing=4),
                   tr("A Pokemon-styled edition of pokeldn {version} by Decryptu, for FireRed and LeafGreen. "
                      "pokeldn is AGPLv3; Pokemon are checked with PKHeX.Core (GPLv3). Not affiliated with "
                      "Nintendo, Game Freak or The Pokemon Company.", version=__version__)),
        ]

    def _language(self, e) -> None:
        self.save("ui_language", e.control.value)
        self.app.relocalize()

    def _my_trainer_editor(self) -> ft.Control:
        """The player's trainer as the game's trainer card shows it; editing marks it typed by hand."""
        s = self.app.settings
        mine = dict(s.my_trainer)

        def store(key, value):
            current = dict(self.app.settings.my_trainer)
            current[key] = value
            current["source"] = "manual"
            current.setdefault("name", "")
            self.app.settings.my_trainer = current
            self.app.settings.save()
            for listener in list(self.app.trainer_listeners):
                listener()

        def number(key, label):
            def changed(e):
                try:
                    value = int(e.control.value)
                except ValueError:
                    return
                if 0 <= value <= 65535:
                    store(key, value)
            return ft.Column([t.text(label, 11, t.MUTED),
                              t.field(value="" if key not in mine else f"{int(mine[key]):05d}", mono=True,
                                      digits=True, limit=5, hint="00000", on_change=changed)],
                             spacing=4, expand=True)

        return ft.Column([
            ft.Row([
                ft.Column([t.text(tr("Name"), 11, t.MUTED),
                           t.field(value=mine.get("name", ""), limit=7,
                                   on_change=lambda e: store("name", e.control.value[:7]))],
                          spacing=4, expand=True),
                ft.Column([t.text(tr("Gender"), 11, t.MUTED),
                           t.dropdown([("0", tr("Boy")), ("1", tr("Girl"))], str(int(mine.get("gender") or 0)),
                                      on_select=lambda e: store("gender", int(e.control.value)))],
                          spacing=4, expand=True),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([number("tid", tr("Trainer ID")), number("sid", tr("Secret ID"))], spacing=10,
                   vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([
                ft.Column([t.text(tr("Game"), 11, t.MUTED),
                           t.dropdown([("firered", tr("FireRed")), ("leafgreen", tr("LeafGreen"))],
                                      mine.get("version") or "firered",
                                      on_select=lambda e: store("version", e.control.value))],
                          spacing=4, expand=True),
                ft.Column([t.text(tr("Language"), 11, t.MUTED),
                           t.dropdown([(k, tr(v)) for k, v in LANGUAGES if k != "8"],
                                      str(int(mine.get("language") or 2)),
                                      on_select=lambda e: store("language", int(e.control.value)))],
                          spacing=4, expand=True),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([t.button(tr("Read from my console"), lambda e: self.app.navigate("games", tool="frlg-trainer"),
                             "trainer")]),
        ], spacing=10)

    def _toggle_advanced(self, e) -> None:
        self.show_advanced = not self.show_advanced
        self.render()
        self.control.update()

    def _check_update(self, e) -> None:
        self.asked = True
        self.app.check_update()
        self._update_text()
        self.update_state.update()

    def _update_text(self) -> None:
        release, state = self.app.update, self.app.update_state
        self.update_state.value = {
            "checking": tr("Checking..."),
            "current": tr("You have the latest version ({version}).", version=__version__),
            "offline": tr("GitHub did not answer. Check your connection."),
            "available": tr("pokeldn {version} is available.", version=release.version) if release else "",
        }.get(state, "")
        self.update_state.color = t.GREEN if state == "available" else t.MUTED

    def _update_shown(self) -> None:
        self._update_text()
        if self.shown:
            self.update_state.update()
            if self.asked and self.app.update:
                self.app.navigate("update")
        self.asked = False

    def _clear_sprites(self, e) -> None:
        self.sprite_state.value = tr("{n} files removed", n=CACHE.clear())
        self.sprite_state.update()

    def _storage_refresh(self, inventory=None) -> None:
        if self.storage_work:
            return
        self.storage_work = True
        self.clear_button.disabled = True
        self.storage_state.value = tr("Clearing local files...") if inventory is not None else tr("Checking local files...")
        if self.shown:
            self.app.ui(self.control.update)
        settings = copy.deepcopy(self.app.settings)

        def work():
            try:
                result = storage.clear(inventory, settings) if inventory is not None else None
                found = storage.scan(settings)
                self.app.ui(lambda: self._storage_done(found, result))
            except OSError as error:
                self.app.ui(lambda message=str(error): self._storage_done(storage.Inventory(errors=1),
                                                                          error=message))
            finally:
                if inventory is not None:
                    self.app.storage_busy = False

        threading.Thread(target=work, daemon=True).start()

    def _storage_done(self, inventory, result=None, error="") -> None:
        self.storage_work = False
        self.storage_inventory = inventory
        count = len(inventory.files)
        self.clear_button.disabled = not count
        self.storage_state.value = (tr("{size} can be freed · {count} files", size=storage.size_text(inventory.size), count=count)
                                    if count else tr("No local files to clear."))
        if inventory.errors:
            self.storage_state.value += tr(" Some folders could not be read.")
        if result is not None:
            self.storage_result.value = tr("Freed {size} · {n} files removed.", size=storage.size_text(result.size), n=result.files)
            if result.errors:
                self.storage_result.value += tr(" {n} files could not be removed; try again.", n=result.errors)
            if result.skipped:
                self.storage_result.value += tr(" Files in use or changed since the check were kept.")
        if error:
            self.storage_result.value = tr("Could not clear local files: {error}", error=error)
        self.storage_result.visible = bool(self.storage_result.value)
        if self.shown:
            self.control.update()

    def _clear_local(self, e) -> None:
        if self.storage_work:
            return
        if self.app.busy:
            self.storage_result.value = tr("Finish the current run or board check before clearing local files.")
            self.storage_result.visible = True
            self.storage_result.update()
            return
        inventory = self.storage_inventory
        if not inventory.files:
            self._storage_refresh()
            return

        def close(e):
            self.app.page.pop_dialog()

        def clear(e):
            close(e)
            if self.app.busy or self.storage_work:
                self.storage_result.value = tr("Finish the current run or board check before clearing local files.")
                self.storage_result.visible = True
                self.storage_result.update()
                return
            self.app.storage_busy = True
            self._storage_refresh(inventory)

        self.app.page.show_dialog(t.dialog(
            title=t.text(tr("Clear local files?"), 17, weight=ft.FontWeight.W_800),
            content=ft.Container(t.text(tr("Remove {n} files and free about {size}. This deletes saved session records, logs, temporary offers and unused built Pokemon. Save any records needed for a bug report first. Your received Pokemon, selected offers, keys, firmware and settings are kept.", n=len(inventory.files), size=storage.size_text(inventory.size)), 13, t.MUTED), width=460),
            actions=[t.secondary_button(tr("Cancel"), close), t.button(tr("Clear files"), clear)],
        ))

    def _keys(self, value: str, update: bool = True) -> None:
        self.save("keys", value)
        ok = keys_found(value)
        self.keys_state.content = ft.Row([
            t.pixel_icon("checkbox-on" if ok else "warning-diamond",
                    color=t.GREEN if ok else t.RED),
            t.text(tr("Found") if ok else tr("No file at this path"), 12, t.GREEN if ok else t.RED)], spacing=6)
        if update:
            self.keys_state.update()
