"""The gift builder shared by the Mystery Gift tools: a preset, a gift built in a form, or an opened
file, then a summary of what the console gets. Each game's form lives in its builder module."""

import asyncio
import copy
import os
import threading

import flet as ft

from gui import drop, theme as t
from gui.i18n import tr
from gui.views.pokemon import NamePicker
from gui.views.saves import SavePanel
from gui.views.widgets import PathField
from pokeldn import gifts, pokemon
from pokeldn.app import command, gift_builder, gift_files, saves
from pokeldn.frlg.gift import builder as frlg
from pokeldn.frlg.rom import custom_code
from pokeldn.swsh import gift_builder as swsh

SPECIES_FRLG = [{"id": n, "name": name} for n, name in frlg.species_names()]


def _number(value, default=0):
    # Decimal first: base 0 refuses a leading zero ("025").
    text = str(value).strip() or str(default)
    for base in (10, 0):
        try:
            return int(text, base)
        except ValueError:
            pass
    return default


def _chips(choices, value, on_change) -> ft.Row:
    """A row of pickable capsules, one per (value, label)."""
    row = ft.Row(spacing=6, wrap=True, run_spacing=6)

    def render(selected):
        row.controls = [ft.Container(
            t.text(tr(label), 12, t.TEXT if key == selected else t.MUTED, weight=ft.FontWeight.W_600),
            padding=ft.Padding(12, 6, 12, 6), border_radius=15,
            border=ft.Border.all(1, t.BLUE if key == selected else t.BORDER),
            bgcolor=t.SELECTED if key == selected else None, on_click=lambda e, k=key: pick(k))
            for key, label in choices]

    def pick(key):
        render(key)
        row.update()
        on_change(key)

    render(value)
    return row


class GiftBuilder:
    def __init__(self, games, field):
        self.games, self.field = games, field
        self.app, self.tool = games.app, games.tool
        self.game = gift_builder.GAMES[self.tool.key]
        self.module = gift_builder.module(self.game)
        self.value = gift_builder.normalized(self.game, command.value_of(field, games.values))
        self.when = t.text("", 12, t.MUTED)
        self.effects = ft.Column(spacing=4)
        self.status = t.text("", 12, t.MUTED)
        self.save_button = t.secondary_button(tr("Save gift file"), self._save, "download")

    # State

    @property
    def state(self) -> dict:
        return self.value["build"]

    def commit(self, rebuild=False) -> None:
        self.games.set_value(self.field, self.value, rebuild=rebuild)
        if not rebuild:
            self.show_summary(update=True)

    def edit(self, key, value, rebuild=False, target=None) -> None:
        (self.state if target is None else target)[key] = value
        self.commit(rebuild)

    # Cards

    def cards(self) -> list[ft.Control]:
        mode = self.value["mode"]
        modes = t.segmented([(key, tr(label), icon) for key, label, icon in gift_builder.modes(self.game)], mode,
                            self._mode, wrap=True)
        body = {"preset": self.presets, "event": self.events, "build": self.editor, "file": self.file,
                "save": lambda: SavePanel(self).control()}[mode]()
        self.show_summary()
        if mode == "save":
            summary = ft.Column([self.when, self.effects, self.status], spacing=10)
            return [t.card(tr("Gift"), ft.Column([modes, body], spacing=14)), t.card(tr("Before you start"), summary)]
        actions = [self.save_button]
        if mode == "preset" and self.module.PRESET[self.value["preset"]].state is not None:
            actions.insert(0, t.secondary_button(tr("Customize"), self._customize, "sliders-horizontal"))
        summary = ft.Column([self.when, self.effects, self.status,
                             ft.Row(actions, alignment=ft.MainAxisAlignment.END)], spacing=10)
        gift = drop.target(t.card(tr("Gift"), ft.Column([modes, body], spacing=14)), self._dropped)
        return [gift, t.card(tr("Before you send"), summary)]

    def exts(self) -> tuple[str, ...]:
        return ("pokegift", "wc8") if self.game == "swsh" else ("pokegift", "wc3")

    def _dropped(self, paths: list[str]) -> None:
        """A gift file dropped anywhere on the card opens it."""
        path = next((p for p in paths if drop.suffix(p) in self.exts()), "")
        if path:
            self.value["mode"], self.value["file"] = "file", path
            self.commit(rebuild=True)

    def _mode(self, key) -> None:
        self.value["mode"] = key
        self.commit(rebuild=True)

    def presets(self) -> ft.Control:
        groups: dict[str, list] = {}
        for preset in self.module.PRESETS:
            groups.setdefault(preset.group, []).append(preset)
        selected = self.module.PRESET[self.value["preset"]]
        sections = []
        for group, items in groups.items():
            tiles, body = [], []
            for preset in items:
                if not hasattr(preset, "members"):
                    tiles.append(self._tile(tr(preset.label), tr(preset.summary), preset is selected,
                                            lambda e, k=preset.key: self._pick(k)))
                    continue
                on = preset.settings(self.value["options"].get(preset.key))["on"] if preset is selected else []
                tiles += [self._tile(tr(b.label), tr(b.summary), b.key in on, lambda e, p=preset, k=b.key: self._toggle(p, k),
                                     settings=bool(b.options)) for b in preset.members]
                if on:
                    body.append(self.boost_settings(preset))
            body.insert(0, t.grid(tiles))
            intro = getattr(self.module, "GROUP_INTROS", {}).get(group, "")
            if intro:
                body.insert(0, t.text(tr(intro), 12, t.MUTED))
            sections.append(t.section(tr(group), ft.Column(body, spacing=10)))
        return ft.Column(sections, spacing=14)

    def _tile(self, label, summary, active, on_click, settings=False) -> ft.Control:
        """The preset's name and full description, including any steps needed to use it."""
        head = [t.text(label, 13, weight=ft.FontWeight.W_600, expand=True)]
        if settings:
            head.append(t.pixel_icon("sliders-horizontal", color=t.BLUE if active else t.FAINT,
                                     tooltip=tr("Has settings")))
        return ft.Container(ft.Row([
            t.pixel_icon("checkbox-on" if active else "checkbox", color=t.BLUE if active else t.FAINT),
            ft.Column([ft.Row(head, spacing=6),
                       t.text(summary, 12, t.MUTED)],
                      spacing=1, expand=True),
        ], spacing=10), padding=ft.Padding(10, 8, 10, 8), border_radius=10,
            tooltip=summary, border=ft.Border.all(1, t.BLUE if active else t.BORDER),
            bgcolor=t.SELECTED if active else None, on_click=on_click)

    def _toggle(self, preset, key) -> None:
        """Tick or untick a boost; the first tick from another gift starts the set with that one."""
        chosen = preset.settings(self.value["options"].get(preset.key))
        if self.value["preset"] != preset.key:
            chosen["on"] = [key]
        elif key in chosen["on"]:
            chosen["on"].remove(key)
        else:
            chosen["on"].append(key)
        self.value["preset"], self.value["options"][preset.key] = preset.key, chosen
        self.commit(rebuild=True)

    def boost_settings(self, preset) -> ft.Control:
        """A panel per ticked boost with settings, then the save switch and the room they take."""
        chosen = preset.settings(self.value["options"].get(preset.key))
        self.value["options"][preset.key] = chosen
        panels = []
        for boost in preset.members:
            if boost.key not in chosen["on"] or not boost.options:
                continue
            mine = chosen[boost.key]
            rows = []
            for option in boost.options:
                if not option.choices:
                    rows.append(self.switch_row(tr(option.label), option.key, tr(option.help), mine))
                elif all(len(label) <= 24 for _, label in option.choices):
                    rows.append(t.labeled_control(tr(option.label), _chips(
                        option.choices, mine[option.key], lambda v, k=option.key, m=mine: self.edit(k, v, target=m))))
                else:
                    rows.append(t.labeled_control(tr(option.label), t.dropdown(
                        [(key, tr(label)) for key, label in option.choices], mine[option.key],
                        on_select=lambda e, k=option.key, m=mine: self.edit(k, e.control.value, target=m))))
            panels.append(ft.Container(ft.Column([t.text(tr(boost.label), 13, weight=ft.FontWeight.W_600), *rows],
                                                 spacing=12),
                                       padding=14, border_radius=10, border=ft.Border.all(1, t.BORDER)))
        used, room = preset.size(chosen), frlg.RESIDENT_AREA
        try:
            too_large = preset.built(chosen)[2]
        except ValueError:
            too_large = False
        keep = (t.text(tr("These boosts are always saved in your game.") + " " + tr(frlg.MOM_STEPS), 12, t.MUTED)
                if too_large or "hook-follower" in chosen["on"]
                else self.switch_row(tr(frlg.KEEP.label), "keep", tr(frlg.KEEP.help), chosen))
        meter = ft.Column([
            ft.Row([t.text(tr("Room on the console"), 12, t.MUTED, expand=True),
                    t.text(tr("{used} of {room} bytes", used=used, room=room), 12,
                           t.RED if used > room else t.MUTED)]),
            ft.ProgressBar(value=min(used / room, 1), color=t.RED if used > room else t.BLUE,
                           bgcolor=t.BORDER, bar_height=4, border_radius=2)], spacing=4)
        common = ft.Container(ft.Column([keep, meter, t.text(
            tr("The selected boosts run together. Sending a new selection replaces the boosts already running."),
            12, t.MUTED)],
            spacing=12), padding=14, border_radius=10, border=ft.Border.all(1, t.BORDER))
        return ft.Column([*panels, common], spacing=10)

    def _pick(self, key) -> None:
        self.value["preset"] = key
        self.commit(rebuild=True)

    # Official events

    def events(self) -> ft.Control:
        """Every official card the game's builder ships, filtered by a search and a group."""
        cards = self.module.OFFICIAL.load()
        tiles = ft.Column(spacing=6, tight=True)
        search = t.field(hint=tr("Search: Pikachu, Master Ball, shiny..."), value=self.value.get("event_search", ""))
        group = {"value": self.value.get("event_group", "")}

        def render(update=True):
            words = search.value.casefold().split()
            shown = [c for c in cards if (not group["value"] or c["group"] == group["value"])
                     and all(w in f"{c['label']} {c['group']} {c['summary']}".casefold() for w in words)]
            tiles.controls = t.grid_rows([self._tile(c["label"], c["summary"], c["key"] == self.value["event"],
                                                     lambda e, k=c["key"]: self._event(k)) for c in shown])
            count.value = tr("{n} of {total} cards", n=len(shown), total=len(cards))
            if update:
                tiles.update()
                count.update()

        def filtered(key, value):
            self.value[key] = value
            if key == "event_group":
                group["value"] = value
            render()

        search.on_change = lambda e: filtered("event_search", search.value)
        count = t.text("", 12, t.MUTED)
        render(update=False)
        groups = _chips([("", "All")] + [(g, g) for g in self.module.OFFICIAL.GROUPS], group["value"],
                        lambda k: filtered("event_group", k))
        intro = t.text(tr("Real event cards from the projectpokemon EventsGallery archive. Each one passed the "
                          "game's own card check."), 12, t.MUTED)
        listing = ft.Container(ft.Column([tiles], scroll=ft.ScrollMode.AUTO), height=440)
        return ft.Column([intro, search, groups, count, listing], spacing=10)

    def _event(self, key) -> None:
        self.value["event"] = key
        self.commit(rebuild=True)

    def _customize(self, e) -> None:
        self.value["build"] = copy.deepcopy(self.module.PRESET[self.value["preset"]].state)
        self.value["mode"] = "build"
        self.commit(rebuild=True)

    def file(self) -> ft.Control:
        path = PathField(self.app.picker, lambda: os.path.expanduser("~"), self.value["file"], "file",
                         self.exts(), self._file, single_line=True, droppable=False)
        controls = [t.text(tr("A .pokegift someone shared, or a {kind} Wonder Card.",
                              kind="Sword/Shield .wc8" if self.game == "swsh" else ".wc3"), 12, t.MUTED),
                    path.control]
        if self.game == "frlg":
            icon = NamePicker(self.app, self.game, "species", str(self.value.get("icon") or ""),
                              self._icon, optional=True, names=SPECIES_FRLG)
            controls.append(t.labeled_control(tr("Card icon"), icon.control))
            controls.append(t.text(tr("Leave empty to keep the file's own icon."), 12, t.MUTED))
        return ft.Column(controls, spacing=8)

    def _icon(self, value) -> None:
        number = _number(value)
        self.value["icon"] = number if number else None
        self.commit()

    def _file(self, path) -> None:
        self.value["file"] = path
        self.commit()

    # Build your own

    def editor(self) -> ft.Control:
        kind = self.state.get("kind")
        kinds = t.segmented([(key, tr(label), icon) for key, label, icon in self.module.KINDS], kind,
                            lambda k: self.edit("kind", k, rebuild=True))
        form = getattr(self, f"{self.game}_{kind}")()
        return ft.Column([kinds, form], spacing=14)

    def text_field(self, label, key, target=None, width=None, **kwargs) -> ft.Control:
        target = self.state if target is None else target
        box = t.field(value=str(target.get(key, "")), on_change=lambda e: self.edit(key, e.control.value,
                                                                                     target=target),
                      expand=width is None, width=width, **kwargs)
        return t.labeled_control(label, box, expand=width is None)

    def number_field(self, label, key, target=None, width=96) -> ft.Control:
        target = self.state if target is None else target
        box = t.field(value=str(target.get(key, "")), mono=True, width=width, digits=True,
                      on_change=lambda e: self.edit(key, _number(e.control.value), target=target))
        return t.labeled_control(label, box)

    def name_field(self, label, kind, key, target=None, optional=True) -> ft.Control:
        target = self.state if target is None else target
        names = SPECIES_FRLG if self.game == "frlg" and kind == "species" else None
        picker = NamePicker(self.app, self.game, kind, str(target.get(key) or ""),
                            lambda v: self.edit(key, _number(v), target=target), optional=optional, names=names)
        return t.labeled_control(label, picker.control, expand=True)

    def switch_row(self, label, key, help_, target=None) -> ft.Control:
        target = self.state if target is None else target
        return ft.Row([ft.Column([t.text(label, 13), t.text(help_, 12, t.MUTED)], spacing=1, expand=True),
                       t.switch(bool(target.get(key)), lambda e: self.edit(key, e.control.value, target=target))])

    def moves(self, target) -> ft.Control:
        target.setdefault("moves", [0, 0, 0, 0])

        def picker(n):
            def changed(v):
                target["moves"][n] = _number(v)
                self.commit()
            return t.labeled_control(tr("Move {n}", n=n + 1), NamePicker(
                self.app, self.game, "move", str(target["moves"][n] or ""), changed).control, expand=True)
        return ft.Column([ft.Row([picker(0), picker(1)], spacing=10), ft.Row([picker(2), picker(3)], spacing=10)],
                         spacing=10)

    # FireRed / LeafGreen

    def frlg_card(self) -> ft.Control:
        card = self.state["card"]
        body = card.setdefault("body", ["", "", "", ""])

        def line(n):
            def changed(e):
                body[n] = e.control.value
                self.commit()
            return t.field(value=body[n], hint=tr("Line {n}", n=n + 1), on_change=changed)
        giver = t.dropdown([(key, f"{tr(who)}, {tr(where)}") for key, who, where, *_ in frlg.GIVERS],
                           self.state.get("giver", "deliveryman"),
                           on_select=lambda e: self.edit("giver", e.control.value, rebuild=True))
        card_form = ft.Column([
            ft.Row([self.text_field(tr("Title"), "title", card), self.text_field(tr("Subtitle"), "subtitle", card)],
                   spacing=10),
            t.labeled_control(tr("Text on the card"), ft.Column([line(n) for n in range(4)], spacing=6,
                                                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            ft.Row([self.name_field(tr("Icon"), "species", "icon", card, optional=False),
                    self.number_field(tr("Card id"), "flag_id", card)], spacing=10),
            self.switch_row(tr("Can be received again"), "repeatable", tr("Otherwise once per save."), card),
            self.switch_row(tr("The player can share it"), "shareable", tr("Mystery Gift, Wonder Cards, Send."), card),
        ], spacing=10)
        return ft.Column([
            t.section(tr("The card"), card_form),
            t.section(tr("Who hands it over"), giver),
            t.section(tr("What happens"), self.frlg_steps()),
        ], spacing=18)

    def frlg_steps(self) -> ft.Control:
        steps = self.state["steps"]
        rows = [self.frlg_step(n, step) for n, step in enumerate(steps)]
        adders = ft.Row([t.secondary_button(tr(label), lambda e, k=key: self._add_step(k), "plus")
                         for key, label in frlg.STEPS], spacing=6, wrap=True, run_spacing=6)
        return ft.Column([*rows, adders], spacing=10)

    def frlg_step(self, n, step) -> ft.Control:
        kind = step["type"]
        label = dict(frlg.STEPS)[kind]
        if kind in ("pokemon", "battle"):
            fields = [ft.Row([self.name_field(tr("Species"), "species", "species", step, optional=False),
                              self.number_field(tr("Level"), "level", step, 72),
                              self.name_field(tr("Held item"), "item", "item", step)], spacing=10)]
            if kind == "pokemon":
                fields.append(self.moves(step))
        elif kind == "egg":
            fields = [self.name_field(tr("Species"), "species", "species", step, optional=False)]
        elif kind == "item":
            fields = [ft.Row([self.name_field(tr("Item"), "item", "item", step, optional=False),
                              self.number_field(tr("How many"), "quantity", step, 72)], spacing=10)]
        else:
            fields = [self.text_field(tr("Message"), "text", step, multiline=True, min_lines=2, max_lines=4,
                                      hint=tr("{PLAYER} is the player's name. A box holds two lines."))]
        tools = ft.Row([t.icon_button("chevron-up", lambda e: self._move_step(n, -1), tr("Earlier"),
                                      disabled=n == 0),
                        t.icon_button("chevron-down", lambda e: self._move_step(n, 1), tr("Later"),
                                      disabled=n == len(self.state["steps"]) - 1),
                        t.icon_button("close", lambda e: self._remove_step(n), tr("Remove"))], spacing=0)
        head = ft.Row([t.text(f"{n + 1}. {tr(label)}", 12, t.SOFT, weight=ft.FontWeight.W_600, expand=True), tools],
                      vertical_alignment=ft.CrossAxisAlignment.CENTER)
        return ft.Container(ft.Column([head, *fields], spacing=8), padding=12, border_radius=10,
                            border=ft.Border.all(1, t.BORDER))

    def _add_step(self, kind) -> None:
        defaults = {"pokemon": {"species": 25, "level": 5, "item": 0, "moves": [0, 0, 0, 0]},
                    "battle": {"species": 25, "level": 5, "item": 0}, "egg": {"species": 25},
                    "item": {"item": 1, "quantity": 1}, "message": {"text": "Here you go!"}}
        self.state["steps"].append({"type": kind, **defaults[kind]})
        self.commit(rebuild=True)

    def _move_step(self, n, delta) -> None:
        steps = self.state["steps"]
        steps[n], steps[n + delta] = steps[n + delta], steps[n]
        self.commit(rebuild=True)

    def _remove_step(self, n) -> None:
        del self.state["steps"][n]
        self.commit(rebuild=True)

    def frlg_news(self) -> ft.Control:
        news = self.state["news"]

        def lines(e):
            news["lines"] = e.control.value.split("\n")[:10]
            self.commit()
        return ft.Column([
            ft.Row([self.text_field(tr("Title"), "title", news), self.number_field(tr("News id"), "id", news)], spacing=10),
            t.labeled_control(tr("Text, up to ten lines"), t.field(value="\n".join(news.get("lines", ())),
                                                               multiline=True, min_lines=4, max_lines=10,
                                                               on_change=lines)),
            t.text(tr("A console keeps news only when it differs from the one it holds; change the id to send "
                      "the same text again."), 12, t.MUTED),
        ], spacing=10)

    def frlg_code(self) -> ft.Control:
        code = self.state["code"]
        self.check_line = t.text("", 12, t.MUTED)
        self.hex_view = t.text("", 11, t.SOFT, font_family=t.MONO, selectable=True)
        source = t.field(value=code.get("source", ""), mono=True, multiline=True, min_lines=10, max_lines=24,
                         on_change=lambda e: code.__setitem__("source", e.control.value),
                         on_blur=lambda e: self.commit())
        binary = PathField(self.app.picker, lambda: os.path.expanduser("~"), code.get("binary", ""), "file",
                           ("bin",), lambda v: self.edit("binary", v, target=code), single_line=True)
        return ft.Column([
            t.text(tr("ARM code runs on the console while it receives, every frame until it returns 1. "
                      "A fault or a loop hangs the Mystery Gift menu, so it is run offline first."), 12, t.MUTED),
            t.labeled_control(tr("Assembly"), source, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            self._toolchain_status(),
            t.labeled_control(tr("Or a prebuilt .bin (used instead of the assembly)"), binary.control),
            ft.Row([t.labeled_control(tr("Built for"), t.dropdown(
                        [("any", tr("Any cartridge"))] + [(k, tr(v)) for k, v in frlg.CARTRIDGES.items()],
                        code.get("build") or "any",
                        on_select=lambda e: self.edit("build", "" if e.control.value == "any" else e.control.value,
                                                      target=code)), expand=True),
                    self.text_field(tr("Expected answer"), "expect", code, width=140, hint=tr("any")),
                    self.text_field(tr("Bytes sent back"), "dump_size", code, width=140, hint="4")], spacing=10),
            ft.Row([t.secondary_button(tr("Check offline"), self._check, "play"), ft.Container(self.check_line,
                                                                                            expand=True)]),
            self.hex_view,
        ], spacing=10)

    def _toolchain_status(self) -> ft.Control:
        if custom_code.toolchain():
            return t.text(tr("Assembled with the GNU Arm toolchain on this computer."), 12, t.MUTED)
        command, page = custom_code.install_hint()
        run = self.app.page.run_task
        if command:
            how = ft.Row([ft.Container(t.text(command, 12, t.TEXT, font_family=t.MONO, selectable=True),
                                       expand=True),
                          t.icon_button("copy", lambda e: run(self.app.copy, command), tr("Copy"))],
                         vertical_alignment=ft.CrossAxisAlignment.CENTER)
            steps = tr("paste this in a terminal, then check again")
        else:
            how, steps = None, tr("download it from Arm's page, then check again")
        actions = ft.Row([t.secondary_button(tr("Check again"), lambda e: self.commit(rebuild=True), "refresh"),
                          t.link_button("Homebrew" if page == "https://brew.sh" else tr("Arm's download page"),
                                        lambda e: run(self.app.open_url, page))], spacing=8)
        return t.surface(ft.Column([
            t.text(tr("Typing assembly here needs the free GNU Arm assembler. Install it once: "
                      "{steps}. A prebuilt .bin works without it.", steps=steps), 12, t.AMBER),
            *([how] if how else []), actions], spacing=8), padding=12)

    def _check(self, e) -> None:
        self.check_line.value, self.check_line.color = tr("Checking…"), t.MUTED
        self.check_line.update()
        code_state = dict(self.state["code"])

        def run():
            try:
                code = frlg.code_bytes(code_state)
                result, color = frlg.checked(code).describe(), t.GREEN
                dump = "\n".join(code[i:i + 16].hex(" ") for i in range(0, min(len(code), 256), 16))
            except (OSError, ValueError) as exc:
                result, color, dump = str(exc), t.RED, ""

            def show():
                self.check_line.value, self.check_line.color, self.hex_view.value = result, color, dump
                self.check_line.update()
                self.hex_view.update()
            self.app.ui(show)
        threading.Thread(target=run, daemon=True).start()

    # Sword / Shield

    def swsh_pokemon(self, egg=False) -> ft.Control:
        rows = [ft.Row([self.name_field(tr("Species"), "species", "species", optional=False),
                        *([] if egg else [self.number_field(tr("Level"), "level", width=72)])], spacing=10)]
        if not egg:
            rows += [ft.Row([self.name_field(tr("Held item"), "bag", "item"), self.name_field(tr("Ball"), "ball", "ball")],
                            spacing=10),
                     ft.Row([self.text_field(tr("Nickname"), "nickname", limit=12),
                             self.text_field(tr("OT"), "ot", limit=12)], spacing=10),
                     self.switch_row(tr("Shiny"), "shiny", tr("The Pokemon arrives shiny.")),
                     self.switch_row("Gigantamax", "gigantamax",
                                     tr("It can Gigantamax; only species with a Gigantamax form."))]
        rows += [self.moves(self.state), self.number_field(tr("Card id"), "card_id")]
        return ft.Column(rows, spacing=10)

    def swsh_egg(self) -> ft.Control:
        return self.swsh_pokemon(egg=True)

    def swsh_items(self) -> ft.Control:
        items = self.state.setdefault("items", [[1, 1]])

        def row(n):
            def item(v):
                items[n][0] = _number(v)
                self.commit()

            def quantity(e):
                items[n][1] = _number(e.control.value)
                self.commit()

            def remove(e):
                del items[n]
                self.commit(rebuild=True)
            return ft.Row([t.labeled_control(tr("Item"), NamePicker(self.app, "swsh", "bag", str(items[n][0] or ""),
                                                                item, optional=False).control, expand=True),
                           t.labeled_control(tr("How many"), t.field(value=str(items[n][1]), mono=True, width=72, digits=True,
                                                                 on_change=quantity)),
                           ft.Container(t.icon_button("close", remove, tr("Remove")), height=t.CONTROL_HEIGHT,
                                        alignment=ft.Alignment.CENTER)],
                          spacing=10, vertical_alignment=ft.CrossAxisAlignment.END)

        def add(e):
            items.append([1, 1])
            self.commit(rebuild=True)
        adder = [t.secondary_button(tr("Add an item"), add, "plus")] if len(items) < 6 else []
        return ft.Column([*(row(n) for n in range(len(items))), *adder, self.number_field(tr("Card id"), "card_id")],
                         spacing=10)

    def swsh_clothing(self) -> ft.Control:
        chosen = self.state.setdefault("outfits", [])

        def toggle(key, on):
            if on and key not in chosen:
                chosen.append(key)
            elif not on and key in chosen:
                chosen.remove(key)
            self.commit()
        rows = [ft.Row([t.text(o.label, 13, expand=True),
                        t.switch(o.key in chosen, lambda e, k=o.key: toggle(k, e.control.value))])
                for o in swsh.OUTFITS]
        return ft.Column([t.text(tr("Official outfits. A card holds six pieces for each gender; the player gets the "
                                    "version for their own."), 12, t.MUTED), *rows,
                          self.number_field(tr("Card id"), "card_id")], spacing=8)

    def swsh_money(self) -> ft.Control:
        return ft.Row([self.number_field(tr("Money"), "money", width=120), self.number_field(tr("Card id"), "card_id")],
                      spacing=10)

    def swsh_bp(self) -> ft.Control:
        return ft.Row([self.number_field(tr("Battle Points"), "bp"), self.number_field(tr("Card id"), "card_id")],
                      spacing=10)

    # Summary

    def name(self, kind, n) -> str:
        """The name PKHeX gives an id; the first miss loads the list and redraws the summary."""
        if self.game == "frlg" and kind == "species":
            return frlg.species_name(n)
        names = "items" if kind == "item" else kind
        cached = pokemon.SERVICE.species_cache.get(f"{self.game}:{names}")
        if cached is None:
            def load():
                try:
                    pokemon.SERVICE.names(self.game, names)
                except Exception:
                    return
                if self.games.tool is self.tool:
                    self.app.ui(lambda: self.show_summary(update=True))
            threading.Thread(target=load, daemon=True).start()
        return next((entry["name"] for entry in cached or () if entry["id"] == _number(n)), f"{kind} #{n}")

    def show_summary(self, update=False) -> None:
        mode = self.value["mode"]
        self.status.value, self.status.color = "", t.MUTED
        if mode == "build":
            when, lines = self.module.describe(self.state, self.name)
        elif mode == "preset":
            preset = self.module.PRESET[self.value["preset"]]
            when, lines = getattr(preset, "when", ""), [preset.summary]
            if hasattr(preset, "members"):
                when = tr("Starts on the console as soon as it is received.")
                lines = preset.effects(self.value["options"].get(preset.key))
            elif preset.state is not None:
                when, lines = self.module.describe(preset.state, self.name)
        elif mode == "save":
            when, lines = self.save_summary()
        elif mode == "event":
            when, lines = self.module.OFFICIAL.describe(self.module.OFFICIAL.by_key()[self.value["event"]]["record"],
                                                      self.name)
        else:
            when, lines = "", []
        problem = gift_builder.problem(self.tool, self.value)
        if problem:
            self.status.value, self.status.color = tr(problem), t.RED
        elif mode == "save":
            pass
        elif mode != "preset" or self.module.PRESET[self.value["preset"]].args == ():
            gift = gift_builder.compile(self.tool, self.value)
            targets = [frlg.CARTRIDGES.get(code, "Sword and Shield") for code in gift.variants]
            self.status.value = tr("Works on {targets}.", targets=", ".join(tr(target) for target in targets))
            if mode == "file":
                lines = [gift.name]
        self.when.value = tr(when)
        self.when.visible = bool(when)
        self.effects.controls = [ft.Row([t.pixel_icon("check", color=t.GREEN), t.text(tr(line), 13, expand=True)],
                                        spacing=8) for line in lines]
        if update:
            for control in (self.when, self.effects, self.status):
                control.update()

    def save_summary(self) -> tuple[str, list[str]]:
        chosen = self.value["save"]
        if chosen["action"] == "backup":
            return (tr("On the console: Mystery Gift, Wonder Cards, Friend, then POKELDN."),
                    [tr("The whole save comes to Your saves, named after the trainer."),
                     tr("The console shows a message and keeps its save as it was.")])
        entry = saves.entry(chosen["file"]) if chosen["file"] else None
        if entry is None:
            return "", []
        return (tr("On the console: Mystery Gift, Wonder Cards, Friend, then POKELDN. Back its save up first."),
                [tr("{name} replaces the console's save.", name=entry.name),
                 tr("The console checks every part, loads it and saves; anything short of that keeps its save."),
                 tr("Then choose CONTINUE on the title screen.")])

    async def select_native_build(self, gift):
        loop = asyncio.get_running_loop()
        chosen = loop.create_future()
        options = [(code, tr(frlg.CARTRIDGES[code])) for code in gift.variants]
        picker = t.dropdown(options, options[0][0])

        async def finish(e):
            if not chosen.done():
                chosen.set_result(picker.value)
            self.app.page.pop_dialog()

        async def cancel(e):
            if not chosen.done():
                chosen.set_result(None)
            self.app.page.pop_dialog()

        async def dismissed(e):
            if not chosen.done():
                chosen.set_result(None)

        self.app.page.show_dialog(t.dialog(
            title=t.text(tr("Export for which cartridge?"), 18, t.TEXT),
            content=ft.Column([
                t.text(tr("A .wc3 holds one cartridge's gift. Choose its version and language. "
                          "A .pokegift keeps every supported cartridge together."), 13, t.MUTED),
                t.labeled_control(tr("Cartridge"), picker),
            ], tight=True, spacing=12, width=420),
            actions=[t.button(tr("Cancel"), cancel, filled=False), t.button(tr("Export"), finish)],
            on_dismiss=dismissed))
        return await chosen

    async def _save(self, e) -> None:
        self.save_button.disabled = True
        self.status.value, self.status.color = tr("Preparing gift file…"), t.MUTED
        self.save_button.update()
        self.status.update()
        tool, extra = self.tool, dict(self.games.extra)
        values = {**self.games.values, self.field.key: copy.deepcopy(self.value)}
        try:
            gift = await asyncio.to_thread(gift_files.build, tool, values, extra, self.app.settings)
            native = "wc8" if self.game == "swsh" else "wc3"
            path = await self.app.picker.save_file(
                dialog_title=tr("Save Mystery Gift"), file_name=f"{tool.key}.pokegift",
                file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=[gifts.EXTENSION, native])
            if path:
                path += "" if path.lower().endswith((".pokegift", f".{native}")) else ".pokegift"
                build = None
                if self.game == "frlg" and path.lower().endswith(".wc3") and len({
                        (v.data.get("card"), v.data.get("ram_script")) for v in gift.variants.values()}) > 1:
                    build = await self.select_native_build(gift)
                    if build is None:
                        self.show_summary()
                        return
                gifts.save(path, gift, build=build)
                self.status.value = tr("Saved {path}", path=path)
            else:
                self.show_summary()
        except (OSError, ValueError, pokemon.BuilderError) as exc:
            self.status.value, self.status.color = tr(str(exc)), t.RED
        finally:
            self.save_button.disabled = False
            if self.games.tool is tool:
                self.save_button.update()
                self.status.update()
