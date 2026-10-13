"""The GTS: banked Pokemon listed against a wanted species on public relays, other players' listings,
and offers on them [pokeldn.app.gts, docs/online.md, The GTS]."""
import re
import threading
import time

import flet as ft

from gui import theme as t
from gui.i18n import tr
from gui.views.bank import NAMES, game_icon, summary_text
from gui.views.sprites import MINI, SIZE, Sprite
from pokeldn import __version__, pokemon
from pokeldn.app import bank
from pokeldn.app.gts import GtsError, Service
from pokeldn.app.paths import GTS
from pokeldn.online import gts

ANY = "-"
# The labels are keys of gui.i18n.ES, translated where they are drawn.
STATUS = {"active": ("Listed", t.BLUE, "globe"), "traded": ("Traded", t.GREEN, "checkbox-on"),
          "withdrawn": ("Taken down", t.MUTED, "close"), "ended": ("Ended", t.MUTED, "clock"),
          "waiting": ("Waiting for the lister", t.BLUE, "clock"), "returned": ("Back in the bank", t.AMBER, "repeat")}


def service(app) -> Service:
    """The app's one GTS client, started on first use; it answers offers while the app is open."""
    if getattr(app, "gts", None) is None:
        # poke-app lists under the player's own trainer, read from the console, when it is known.
        app.gts = Service(trainer=app.settings.my_trainer.get("name") or app.settings.ot, app=__version__)
        app.gts.start()
    return app.gts


def resume(app) -> None:
    """Start the client when an earlier session left a listing or an offer to settle."""
    if GTS.is_dir() and any(GTS.glob("*/state.json")):
        service(app)


def level_of(entry: bank.Entry) -> int:
    found = re.search(r"level (\d+)", entry.summary)
    return int(found.group(1)) if found else 0


def _when(seconds: float) -> str:
    return time.strftime("%d %b %Y", time.localtime(seconds))


def wants_text(wants: gts.Wants) -> str:
    """gts.Wants.text in the app's language."""
    if (wants.min_level, wants.max_level) == (1, 100):
        return wants.name
    return tr("{name}, level {low} to {high}", name=wants.name, low=wants.min_level, high=wants.max_level)


def reason(text: str) -> str:
    """A reason pokeldn.app.gts gives (a GtsError, or why an offer came back) in the app's language. The fixed
    ones are keys of their own; these carry a species, levels or PKHeX's own words. Anything else stays as is."""
    body, end = (text[:-1], ".") if text.endswith(".") else (text, "")
    if found := re.fullmatch(r"PKHeX could not read it \((.*)\)", body, re.DOTALL):
        return tr("PKHeX could not read it ({error})", error=found[1]) + end
    if found := re.fullmatch(r"PKHeX finds it not legal \((.*)\)", body, re.DOTALL):
        return tr("PKHeX finds it not legal ({report})", report=found[1]) + end
    if found := re.fullmatch(r"The lister asks for level (\d+) to (\d+)\.", text):
        return tr("The lister asks for level {low} to {high}.", low=found[1], high=found[2])
    if found := re.fullmatch(r"The lister asks for (.+)\.", text):
        return tr("The lister asks for {name}.", name=found[1])
    return tr(text)


class GtsView:
    def __init__(self, app):
        self.app = app
        self.visible = False
        self.species: list[tuple[str, str]] = []      # (id, name), every game's
        self.search = "has"
        self.chosen = ANY
        self.selected: tuple | str = ""                 # a listing's (key, d), or one of ours by id
        self.working = False
        self.pending = False
        self.status = t.text("", 12, t.MUTED)
        self.mine = ft.Column(spacing=2)
        self.grid = ft.Row(spacing=8, run_spacing=8, wrap=True)
        self.heading = t.text("", 12, t.MUTED)
        self.detail = ft.Column(spacing=24, scroll=ft.ScrollMode.AUTO, expand=True)
        self.note = t.text("", 12, t.MUTED)
        self.picker = t.dropdown([(ANY, tr("Any Pokemon"))], ANY, self._pick, enable_filter=True, editable=True,
                                 menu_height=320)
        self.control = ft.Row([
            t.panel(ft.Column([
                t.panel_header(tr("GTS"), t.icon_button("refresh", lambda e: self._browse(), tr("Look again"))),
                ft.Container(ft.Column([
                    self.status,
                    t.segmented([("has", tr("Offered"), "package"), ("wants", tr("Wanted"), "search")], self.search,
                                self._mode),
                    self.picker,
                    t.button(tr("Deposit a Pokemon"), lambda e: self._deposit_dialog(), "upload"),
                    t.section(tr("Yours"), self.mine),
                ], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True), padding=ft.Padding(14, 4, 14, 14),
                    expand=True),
            ], spacing=0, expand=True), width=t.SIDEBAR_WIDTH),
            t.fade(ft.ListView([ft.Container(self.heading, padding=ft.Padding(4, 14, 4, 0)), self.grid],
                               spacing=12, padding=ft.Padding(0, 0, 0, 24), expand=True)),
            t.panel(ft.Column([
                t.panel_header(tr("Listing")),
                ft.Container(ft.Column([self.detail, self.note], spacing=8, expand=True),
                             padding=ft.Padding(18, 8, 18, 18), expand=True),
            ], spacing=0, expand=True), width=t.SESSION_WIDTH),
        ], spacing=t.GAP, expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)

    @property
    def client(self) -> Service:
        return service(self.app)

    def enter(self, **_) -> None:
        self.visible = True
        if self._changed not in self.client.listeners:
            self.client.listeners.append(self._changed)
        if not self.species:
            threading.Thread(target=self._load_species, daemon=True).start()
        self._browse(update=False)
        self.render()

    def leave(self) -> None:
        self.visible = False

    def _load_species(self) -> None:
        names: dict[int, str] = {}
        for game in NAMES:
            try:
                names.update((s["id"], s["name"]) for s in pokemon.SERVICE.species(game))
            except (OSError, pokemon.BuilderError):
                continue

        def done():
            self.species = sorted(((str(k), v) for k, v in names.items()), key=lambda s: s[1])
            self.picker.options = [ft.DropdownOption(key=ANY, text=tr("Any Pokemon"))] + [
                ft.DropdownOption(key=k, text=v) for k, v in self.species]
            if self.visible:
                self.picker.update()
        self.app.ui(done)

    def _changed(self) -> None:
        """From a relay thread: draw again once, however many events arrive together."""
        if self.pending or not self.visible:
            return
        self.pending = True

        def draw():
            self.pending = False
            if self.visible:
                self.render()
                self.control.update()
        self.app.ui(draw)

    # Searching

    def _filters(self) -> dict:
        species = int(self.chosen) if self.chosen not in (None, ANY) else None
        return {"has": species} if self.search == "has" else {"wants": species}

    def _browse(self, update=True) -> None:
        self.client.browse(**self._filters())
        if update:
            self.render()
            self.control.update()

    def _mode(self, key: str) -> None:
        self.search = key
        self._browse()

    def _pick(self, e) -> None:
        self.chosen = e.control.value or ANY
        self._browse()

    # Drawing

    def render(self) -> None:
        client = self.client
        relays = client.connected()
        listings = client.open_listings(**self._filters())
        self.status.value = (tr("{n} of {total} relays connected", n=relays, total=len(gts.relay_urls())) if relays
                             else tr("Connecting to the relays..."))
        if listings:
            self.heading.value = (tr("1 open listing") if len(listings) == 1
                                  else tr("{n} open listings", n=len(listings)))
        elif client.loaded():
            self.heading.value = tr("No open listing matches. Deposit one of yours from the left.")
        else:
            self.heading.value = tr("Reading the listings from the relays...")
        self.grid.controls = [self._tile(x) for x in listings]
        self.mine.controls = [self._mine_row(s) for s in client.mine()] or [
            t.text(tr("Nothing listed or offered."), 12, t.FAINT)]
        self.render_detail(listings)

    def _tile(self, listing: gts.Listing) -> ft.Control:
        active = self.selected == (listing.key, listing.d)
        shown = listing.pokemon
        return ft.Container(ft.Row([
            ft.Stack([Sprite(self.app, int(shown.get("species_id") or 0), bool(shown.get("shiny")), size=MINI).control,
                      ft.Container(game_icon(listing.game, 16), right=0, bottom=0)]),
            t.pixel_icon("arrows-horizontal", size=12, color=t.FAINT),
            Sprite(self.app, listing.wants.species, size=MINI).control,
        ], spacing=4, tight=True), padding=4, border_radius=14,
            tooltip=tr("{species} level {level} for {wants}", species=shown.get("species"), level=shown.get("level"),
                       wants=wants_text(listing.wants)),
            border=ft.Border.all(2, t.BLUE if active else ft.Colors.TRANSPARENT),
            on_click=lambda e, k=(listing.key, listing.d): self._select(k))

    def _mine_row(self, state: dict) -> ft.Control:
        label, color, icon = STATUS[state["status"]]
        species = state["info"].get("species", "")
        if state["role"] == "listing":
            title = tr("{species} for {name}", species=species, name=gts.Wants(**state["wants"]).name)
        else:
            title = tr("{species} offered for {name}", species=species,
                       name=state["listing"] and gts.parse_listing(state["listing"]).pokemon.get("species"))
        active = self.selected == state["id"]
        return ft.Container(ft.Row([
            Sprite(self.app, int(state["info"].get("species_id") or 0), bool(state["info"].get("shiny")),
                   size=MINI).control,
            ft.Column([t.text(title, 12, t.TEXT, weight=ft.FontWeight.W_600, max_lines=1,
                              overflow=ft.TextOverflow.ELLIPSIS),
                       t.badge(tr(label), color, icon)], spacing=2, expand=True),
        ], spacing=8), padding=ft.Padding(4, 4, 6, 4), border_radius=12,
            bgcolor=t.SELECTED if active else None, on_click=lambda e, i=state["id"]: self._select(i))

    def _select(self, key) -> None:
        self.selected = key
        self.note.value = ""
        self.render()
        self.control.update()

    def render_detail(self, listings: list[gts.Listing]) -> None:
        if isinstance(self.selected, str) and self.selected:
            state = next((s for s in self.client.mine() if s["id"] == self.selected), None)
            if state:
                self.detail.controls = self._mine_detail(state)
                return
        listing = next((x for x in listings if (x.key, x.d) == self.selected), None)
        if listing is None:
            self.detail.controls = [t.text(tr(
                "Pick a listing to see the Pokemon and what its trainer asks for. A trade happens the next time "
                "the lister's app is open; until then your offer waits outside your bank."), 13, t.MUTED)]
            return
        asks = ft.Row([Sprite(self.app, listing.wants.species, size=MINI).control,
                       t.text(wants_text(listing.wants), 13)], spacing=10)
        self.detail.controls = [self._about(listing.pokemon, listing.game),
                                t.section(tr("Asks for"), asks),
                                t.text(tr("From {trainer}, open until {date}", trainer=listing.trainer or tr("a trainer"),
                                          date=_when(listing.expires)), 12, t.FAINT),
                                t.section(tr("Your Pokemon that answer it"), self._answers(listing))]

    def _about(self, shown: dict, game: str) -> ft.Control:
        facts = [shown.get("nature"), shown.get("ability"), shown.get("ball")]
        if shown.get("held_item"):
            facts.append(tr("holding {item}", item=shown["held_item"]))
        return ft.Row([
            Sprite(self.app, int(shown.get("species_id") or 0), bool(shown.get("shiny")), size=SIZE).control,
            ft.Column([
                t.text(" · ".join([str(shown.get("species")), tr("level {level}", level=shown.get("level"))]
                                  + ([tr("shiny")] if shown.get("shiny") else [])),
                       15, weight=ft.FontWeight.W_600),
                t.text(" · ".join(str(f) for f in facts if f), 12, t.MUTED),
                t.text(", ".join(shown.get("moves") or []), 12, t.MUTED),
                ft.Row([game_icon(game), t.text(tr("In {game}, OT {ot}", game=tr(NAMES.get(game, game)),
                                                   ot=shown.get("ot")), 12, t.SOFT)],
                       spacing=6),
            ], spacing=4, expand=True),
        ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.START)

    def _answers(self, listing: gts.Listing) -> ft.Control:
        held = [e for e in bank.entries() if e.species_id == listing.wants.species and e.legal
                and not listing.wants.refusal(e.species_id, level_of(e))
                and not bank.queued(self.app.settings, e.id)]
        if not held:
            return t.text(tr("Your bank holds no legal {wants} that is not queued for a trade.",
                             wants=wants_text(listing.wants)), 12, t.FAINT)
        return ft.Column([ft.Row([
            Sprite(self.app, e.species_id, e.shiny, size=MINI).control,
            ft.Column([t.text(summary_text(e.summary), 12, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                       ft.Row([game_icon(e.game, 16), t.text(tr(NAMES[e.game]), 11, t.MUTED)], spacing=4)],
                      spacing=2, expand=True),
            t.button(tr("Offer"), lambda ev, x=e: self._confirm_offer(listing, x), "arrows-horizontal",
                     disabled=self.working),
        ], spacing=8) for e in held], spacing=8)

    def _mine_detail(self, state: dict) -> list[ft.Control]:
        label, color, icon = STATUS[state["status"]]
        controls = [self._about(state["info"], state["game"]), t.badge(tr(label), color, icon)]
        if state["role"] == "listing":
            wants, answered, until = gts.Wants(**state["wants"]), len(state["answers"]), _when(state["expires"])
            controls.append(t.text(
                tr("Asks for {wants}. Open until {date}; 1 offer answered.", wants=wants_text(wants), date=until)
                if answered == 1 else
                tr("Asks for {wants}. Open until {date}; {n} offers answered.", wants=wants_text(wants), date=until,
                   n=answered), 12, t.MUTED))
            if state["status"] == "traded":
                controls.append(t.text(tr("Traded with {name}; what came back is in the bank.",
                                          name=state["partner"] or tr("a trainer")), 12, t.SOFT))
            if state["status"] == "active":
                controls.append(t.secondary_button(tr("Take it down"), lambda e: self._withdraw(state), "close"))
        else:
            listing = gts.parse_listing(state["listing"])
            if listing:
                controls.append(t.text(tr("Offered for {species} level {level} from {trainer}.",
                                          species=listing.pokemon.get("species"), level=listing.pokemon.get("level"),
                                          trainer=listing.trainer or tr("a trainer")), 12, t.MUTED))
            if state["status"] == "waiting":
                controls.append(t.text(tr("The trade happens the next time the lister's app is open. If it ends "
                                          "unanswered, your Pokemon comes back to the bank."), 12, t.FAINT))
            if state["why"]:
                controls.append(t.text(reason(state["why"][0].upper() + state["why"][1:] + "."), 12,
                                       t.AMBER if state["status"] == "returned" else t.SOFT))
        if state["status"] not in ("active", "waiting"):
            controls.append(t.secondary_button(tr("Clear from the list"), lambda e: self._forget(state), "trash"))
        return controls

    # Actions

    def _work(self, label: str, action, done_text: str) -> None:
        self.working = True
        self._say(label, t.BLUE)

        def work():
            try:
                action()
                problem = ""
            except (OSError, GtsError, pokemon.BuilderError) as error:
                problem = str(error)

            def done():
                self.working = False
                self.render()
                self.control.update()
                self._say(reason(problem) if problem else done_text, t.RED if problem else t.MUTED)
            self.app.ui(done)
        threading.Thread(target=work, daemon=True).start()

    def _confirm_offer(self, listing: gts.Listing, entry: bank.Entry) -> None:
        def go(e):
            self.app.page.pop_dialog()
            self._work(tr("PKHeX is checking it..."), lambda: self.client.offer(listing, entry),
                       tr("Offered. Yours lists the answer once the lister's app sends it."))

        self.app.page.show_dialog(t.dialog(
            title=t.text(tr("Offer {name}?", name=entry.summary.split(" · ")[0]), 18),
            content=t.text(tr("It leaves your bank and waits for the lister's app. You get "
                              "{species} if your offer is the first that answers the "
                              "listing; otherwise it comes back. Nothing on the relays can make the lister send "
                              "theirs: a trade depends on the other app being the real one.",
                              species=listing.pokemon.get("species")), 13, t.MUTED, width=400),
            actions=[t.button(tr("Cancel"), lambda e: self.app.page.pop_dialog(), filled=False),
                     t.button(tr("Offer"), go, "arrows-horizontal")]))

    def _withdraw(self, state: dict) -> None:
        self._work(tr("Taking it down..."), lambda: self.client.withdraw(state["id"]),
                   tr("Taken down. The Pokemon is back in the bank."))

    def _forget(self, state: dict) -> None:
        self.client.forget(state["id"])
        self.selected = ""
        self.render()
        self.control.update()

    def _deposit_dialog(self) -> None:
        held = [e for e in bank.entries() if e.legal and not bank.queued(self.app.settings, e.id)]
        if not held:
            self._say(tr("The bank holds no legal Pokemon that is not queued for a trade."), t.AMBER)
            return
        if not self.species:
            self._say(tr("PKHeX is still reading the species list; try again in a moment."), t.AMBER)
            return
        labels = [(e.id, summary_text(e.summary).split(" · "), tr(NAMES[e.game])) for e in held]
        choice = t.dropdown([(i, f"{parts[0]}, {parts[1]} ({game})") for i, parts, game in labels], held[0].id,
                            enable_filter=True, editable=True, menu_height=320)
        wanted = t.dropdown(self.species, None, enable_filter=True, editable=True, menu_height=320)
        low = t.field(value="1", mono=True, width=80, digits=True, limit=3)
        high = t.field(value="100", mono=True, width=80, digits=True, limit=3)
        message = t.text("", 12, t.RED)

        def go(e):
            entry = next((x for x in held if x.id == choice.value), None)
            name = dict(self.species).get(wanted.value or "")
            levels = (low.value or "").strip(), (high.value or "").strip()
            if entry is None or not name:
                message.value = tr("Pick your Pokemon and the one you ask for.")
            elif not all(v.isdigit() for v in levels) or not 1 <= int(levels[0]) <= int(levels[1]) <= 100:
                message.value = tr("The levels go from 1 to 100, the first no higher than the second.")
            else:
                self.app.page.pop_dialog()
                wants = gts.Wants(int(wanted.value), name, int(levels[0]), int(levels[1]))
                self._work(tr("PKHeX is checking it..."), lambda: self.client.deposit(entry, wants),
                           tr("Listed for 30 days. Your app trades it when it is open and a matching offer arrives."))
                return
            message.update()

        self.app.page.show_dialog(t.dialog(
            title=t.text(tr("Deposit a Pokemon"), 18),
            content=ft.Column([
                t.labeled_control(tr("Your Pokemon"), choice),
                t.labeled_control(tr("Ask for"), wanted),
                ft.Row([t.labeled_control(tr("Lowest level"), low), t.labeled_control(tr("Highest level"), high)],
                       spacing=10),
                t.text(tr("It leaves the bank while listed. The first offer that answers it is traded, by this app, "
                          "the next time it is open. Take it down from Yours to get it back."), 12, t.FAINT),
                message,
            ], spacing=14, tight=True, width=420),
            actions=[t.button(tr("Cancel"), lambda e: self.app.page.pop_dialog(), filled=False),
                     t.button(tr("Deposit"), go, "upload")]))

    def _say(self, text: str, color: str) -> None:
        self.note.value, self.note.color = text, color
        try:
            self.note.update()
        except RuntimeError:
            pass
