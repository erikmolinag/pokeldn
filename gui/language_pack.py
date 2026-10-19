"""poke-app's Spanish for upstream's screens: a language pack [docs/plugins.md, Language packs] shipped in
gui/assets/lang/es instead of installed. Upstream looks its text up by key (pokeldn.app.i18n.t) and turns
module messages and game terms through the pack; poke-app's own screens use gui/i18n.py, from the same
choice in Settings (Settings.ui_language)."""
import os
from pathlib import Path

FOLDER = Path(__file__).resolve().parent / "assets" / "lang" / "es"
ID = "poke-app-es"


def install() -> None:
    """Names the bundled pack in POKELDN_PLUGINS, which pokeldn.plugins reads whatever Settings turned on."""
    named = [p for p in os.environ.get("POKELDN_PLUGINS", "").split(os.pathsep) if p]
    if str(FOLDER) not in named:
        os.environ["POKELDN_PLUGINS"] = os.pathsep.join([*named, str(FOLDER)])


def use(code: str) -> None:
    """Selects the pack for Spanish and English for anything else. Text built at import, such as the tool
    catalog, follows at the next start."""
    from pokeldn.app import i18n
    install()
    i18n.select(ID if code == "es" else "")
