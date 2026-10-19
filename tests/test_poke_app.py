"""poke-app: the console's trainer read on the link, kept as the player's own, and the app's own list."""
import ast
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from pokeldn.app import catalog, received, settings as settingsmod  # noqa: E402
from pokeldn.frlg.link import linkplayer  # noqa: E402


def _player(**kw):
    base = dict(name="erks", trainer_id=(18929 << 16) | 59296, version=linkplayer.VERSION_FIRE_RED,
                language=linkplayer.LANGUAGE_ENGLISH, gender=0)
    base.update(kw)
    return linkplayer.LinkPlayer(**base)


def test_the_host_reports_tid_and_sid_from_the_32_bit_id():
    line = "[   62.0s] " + linkplayer.trainer_report(_player())
    assert received.trainer_found(line) == {"name": "erks", "tid": 59296, "sid": 18929, "gender": 0,
                                           "language": 2, "version": "firered"}


def test_a_spanish_leafgreen_girl_reads_back_the_same():
    lp = _player(name="Alberto", trainer_id=0x6FCFD65B, version=linkplayer.VERSION_LEAF_GREEN,
                 language=linkplayer.LANGUAGE_SPANISH, gender=1)
    found = received.trainer_found(linkplayer.trainer_report(lp))
    assert (found["tid"], found["sid"]) == (54875, 28623)
    assert (found["version"], found["language"], found["gender"]) == ("leafgreen", 7, 1)


@pytest.mark.parametrize("line", ["[done] trade 1 complete", "[trainer] {not json}", "[trainer] {\"name\": 1}",
                                  "Console identified as 'erks'"])
def test_other_lines_are_not_a_trainer(line):
    assert received.trainer_found(line) is None


def test_built_pokemon_belong_to_the_players_trainer_once_read(tmp_path, monkeypatch):
    monkeypatch.setattr(settingsmod, "PATH", tmp_path / "settings.json")
    s = settingsmod.Settings(ot="POKELDN", tid=111, sid=222)
    assert s.owner("frlg")["ot"] == "POKELDN"
    report = {"name": "erks", "tid": 59296, "sid": 18929, "gender": 0, "language": 2, "version": "firered"}
    assert s.set_my_trainer(report, "console")
    assert s.owner("frlg") == {"ot": "erks", "tid": 59296, "sid": 18929, "language": 2, "gender": 0}
    assert s.trainer("frlg")["ot"] == "POKELDN"           # the link identity stays pokeldn's
    assert not s.set_my_trainer(report, "console")         # the same report again changes nothing


def test_the_app_lists_firered_and_leafgreen_with_the_trainer_reader_first():
    (game,) = catalog.APP_GAMES
    assert game.key == "frlg"
    first = game.tools[0]
    assert first.key == "frlg-trainer" and "--identify" in first.fixed
    frlg = next(g for g in catalog.GAMES if g.key == "frlg")
    assert [t.key for t in game.tools[1:]] == [t.key for t in frlg.tools]
    assert "frlg-trade-online" in [t.key for t in game.tools]


def test_identify_needs_no_party_file():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frlg_trade_host", os.path.join(ROOT, "bin", "frlg_trade_host.py"))
    host = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(host)
    args = host.build_parser().parse_args(["--identify", "--live"])
    assert args.identify and args.party == []


def _tr_calls(*folders):
    """(file:line, args) of every tr(...) call whose first argument is a literal, in these folders' files."""
    for folder in folders:
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            if not name.endswith(".py"):
                continue
            tree = ast.parse(open(os.path.join(ROOT, folder, name), encoding="utf-8").read())
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr"
                        and node.args and isinstance(node.args[0], ast.Constant)
                        and isinstance(node.args[0].value, str) and node.args[0].value):
                    yield f"{folder}/{name}:{node.lineno}", node.args


def test_every_translated_string_has_a_spanish_entry():
    """poke-app's own English-keyed text has Spanish in gui/i18n.py; upstream's keyed text (tr(key, default))
    has it in the bundled language pack (gui/assets/lang/es)."""
    import tomllib
    from gui import i18n, language_pack
    pack = tomllib.loads((language_pack.FOLDER / "strings.toml").read_text(encoding="utf-8"))
    missing = []
    for where, args in _tr_calls("gui", os.path.join("gui", "views"), os.path.join("pokeldn", "app")):
        key = args[0].value
        keyed = len(args) > 1
        if (keyed and key not in pack) or (not keyed and "pokeldn" not in where and key not in i18n.ES):
            missing.append(f"{where} {key[:60]!r}")
    assert not missing, "\n".join(missing)


def test_the_spanish_pack_translates_every_upstream_key():
    import tomllib
    from gui import language_pack
    english = tomllib.loads(open(os.path.join(ROOT, "pokeldn", "app", "data", "strings.en.toml"), "rb").read().decode())
    spanish = tomllib.loads((language_pack.FOLDER / "strings.toml").read_text(encoding="utf-8"))
    assert not [key for key in english if key not in spanish]
    import string
    fields = lambda text: sorted(f for _, f, _, _ in string.Formatter().parse(text) if f)   # noqa: E731
    assert not [key for key in english if fields(english[key]) != fields(spanish[key])]


def test_tr_falls_back_to_english_and_formats():
    from gui import i18n
    i18n.set_language("es")
    assert i18n.tr("{n} traded", n=3) == "3 intercambiados"
    assert i18n.tr("Not a key at all") == "Not a key at all"
    i18n.set_language("en")
    assert i18n.tr("{n} traded", n=3) == "3 traded"
    i18n.set_language("es")


def test_the_identify_placeholder_builds_through_pkhex():
    """--identify's Pidgey goes through the real helper: a version PKHeX cannot parse failed on retail."""
    from pokeldn import pokemon
    try:
        pokemon._command()
    except Exception:
        pytest.skip("PKHeX helper not built")
    import importlib.util
    spec = importlib.util.spec_from_file_location("frlg_trade_host", os.path.join(ROOT, "bin", "frlg_trade_host.py"))
    host = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(host)
    info = pokemon.SERVICE.check("frlg", host.identify_placeholder())
    assert info["legal"] and info["species_id"] == host.PLACEHOLDER_SPECIES


def test_the_menu_arrows_reach_every_tile_and_lead_back():
    """HOME's tile grid: from any tile the arrows reach every other one, and every move has a way back."""
    pytest.importorskip("flet")
    from gui.views.menu import ENTRIES, MOVES
    back = {"Arrow Up": "Arrow Down", "Arrow Down": "Arrow Up", "Arrow Left": "Arrow Right",
            "Arrow Right": "Arrow Left"}
    assert set(MOVES) == set(range(len(ENTRIES)))
    for start in MOVES:
        seen, todo = {start}, [start]
        while todo:
            for target in MOVES[todo.pop()].values():
                if target not in seen:
                    seen.add(target)
                    todo.append(target)
        assert seen == set(MOVES)
    for moves in MOVES.values():
        for key, target in moves.items():
            assert back[key] in MOVES[target]


def test_the_app_links_only_to_the_fork():
    pytest.importorskip("flet")
    from gui.views import docs, settings as settings_view
    urls = [url for _, url in settings_view.LINKS] + [docs.REPO, docs.SITE]
    assert all(url.startswith("https://github.com/erikmolinag/pokeldn") for url in urls)


def test_the_pokemon_screen_builds_for_the_players_own_trainer():
    """gui/views/pokemon.py builds, reads options and pastes for Settings.owner (the trainer read from the console),
    never for pokeldn's link identity: a merge that took upstream's file whole once lost this."""
    tree = ast.parse(open(os.path.join(ROOT, "gui", "views", "pokemon.py"), encoding="utf-8").read())
    calls = [node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Attribute)
             and node.func.value.attr == "settings" and node.func.attr in ("owner", "trainer")]
    assert calls.count("owner") == 3 and "trainer" not in calls


def test_best_ivs_are_the_best_legal_frame_for_the_trainer_asked():
    """services/pkhex MakeBestIvs against the frames ~/pkgen found for Erik's TID/SID on 2026-09-30: a shiny
    Nidoking's best is 182 (Hardy), and 177 when it must be Hasty. Another trainer gets other frames."""
    from pokeldn import pokemon
    try:
        pokemon._command()
    except Exception:
        pytest.skip("PKHeX helper not built")
    erks = {"ot": "erks", "tid": 59296, "sid": 18929, "language": 2, "gender": 0}
    best = pokemon.SERVICE.make("frlg", 34, erks, 33, True, "", "FR", {"best_ivs": True})
    hasty = pokemon.SERVICE.make("frlg", 34, erks, 33, True, "", "FR", {"best_ivs": True, "nature": 11})
    other = pokemon.SERVICE.make("frlg", 34, {**erks, "ot": "ASH", "tid": 12345, "sid": 54321}, 33, True, "", "FR",
                                 {"best_ivs": True})
    assert best["legal"] and best["shiny"] and sum(best["ivs"]) == 182 and best["nature"] == "Hardy"
    assert (best["ot"], best["trainer_id"], best["secret_id"]) == ("erks", 59296, 18929)
    assert hasty["legal"] and hasty["shiny"] and hasty["nature"] == "Hasty" and hasty["ivs"] == [29, 27, 30, 31, 29, 31]
    assert other["legal"] and other["shiny"] and other["ivs"] != best["ivs"] and other["trainer_id"] == 12345


def test_the_best_ivs_switch_is_frlgs_and_replaces_the_typed_ivs():
    pytest.importorskip("flet")
    from types import SimpleNamespace
    import flet as ft
    from gui import theme as t
    from gui.views.pokemon import OfferOptions
    found = {"natures": [], "abilities": [], "gendered": True, "balls": [], "held": [], "forms": [], "move_names": [],
             "effort": {"kind": "evs", "max": 252, "total": 510}}

    def best_rows(game):
        options = OfferOptions(SimpleNamespace(game=game, value={"options": {"ivs": {"hp": 30}}}))
        options.control.update = lambda: None
        return options, [c for c in options._form(found) if isinstance(c, ft.Container) and c.bgcolor == t.SELECTED]

    assert best_rows("swsh")[1] == []
    options, (row,) = best_rows("frlg")
    switch = row.content.controls[1]
    switch.value = True
    switch.on_change(SimpleNamespace(control=switch))
    assert options.chosen.get("best_ivs") is True and "ivs" not in options.chosen
    switch.value = False
    switch.on_change(SimpleNamespace(control=switch))
    assert "best_ivs" not in options.chosen
