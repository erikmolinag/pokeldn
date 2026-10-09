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


def test_every_translated_string_has_a_spanish_entry():
    from gui import i18n
    missing = []
    for folder in ("gui", os.path.join("gui", "views")):
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            if not name.endswith(".py"):
                continue
            tree = ast.parse(open(os.path.join(ROOT, folder, name), encoding="utf-8").read())
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr"
                        and node.args and isinstance(node.args[0], ast.Constant)
                        and isinstance(node.args[0].value, str) and node.args[0].value
                        and node.args[0].value not in i18n.ES):
                    missing.append(f"{folder}/{name}:{node.lineno} {node.args[0].value[:60]!r}")
    assert not missing, "\n".join(missing)


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
