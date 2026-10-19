"""Builds poke-app's Spanish language pack, gui/assets/lang/es [docs/plugins.md, Language packs], from
upstream's keyed English (pokeldn/app/data/strings.en.toml and every tr(key, default) in the code) and
poke-app's English-keyed Spanish (gui/i18n.py ES).

A key the pack already translates keeps its Spanish. A new key whose English is an ES entry takes that
Spanish, its fields renamed to the key's. ES as a whole becomes the pack's messages (module text shown
through pokeldn.app.i18n.message) and, where it has fields, its templates. What is left untranslated is
written to scratchpad/spanish_todo.json for a translator, then merged back with --merge FILE.

    python scripts/poke_app_spanish_pack.py [--merge translated.json]
"""
import argparse
import ast
import json
import re
import string
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PACK = ROOT / "gui" / "assets" / "lang" / "es"
TODO = ROOT / "scratchpad" / "spanish_todo.json"
SOURCES = ("gui", "gui/views", "pokeldn/app", "pokeldn")
TERMS = {"FireRed": "Rojo Fuego", "LeafGreen": "Verde Hoja", "Poke Ball": "Poké Ball", "Pokedex": "Pokédex"}
PLUGIN = '''id = "poke-app-es"
name = "Español"
version = "1.0.0"
author = "erks"
description = "poke-app's Spanish, bundled with the app."
api = "1.9"
locale = "es"
strings = "strings.toml"
messages = "messages.toml"
templates = "templates.toml"
terms = "terms.toml"
'''


def fields(text: str) -> list[str]:
    try:
        return [f for _, f, _, _ in string.Formatter().parse(text) if f is not None]
    except ValueError:
        return []


def shape(text: str) -> str:
    """The text with every field as {}: two texts of one shape differ only in their fields' names."""
    return re.sub(r"\{[^{}]*\}", "{}", text)


def code_keys() -> dict[str, str]:
    """key -> English default of every tr(key, default) call with literal arguments."""
    found = {}
    for folder in SOURCES:
        for path in sorted((ROOT / folder).glob("*.py")):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("tr", "t")
                        and len(node.args) >= 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str)
                                                         for a in node.args[:2])
                        and re.fullmatch(r"[a-z0-9_]+\.[\w.]+", node.args[0].value)):
                    found.setdefault(node.args[0].value, node.args[1].value)
    return found


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_table(path: Path, table: dict[str, str], header: str) -> None:
    lines = [f"# {header}"] + [f"{toml_string(k)} = {toml_string(v)}" for k, v in sorted(table.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def renamed(spanish: str, ours: str, theirs: str) -> str | None:
    """`spanish` (the translation of `ours`) with ours' fields renamed to theirs', matched by position."""
    a, b = fields(ours), fields(theirs)
    if len(a) != len(b) or len(set(a)) != len(a):
        return None
    names = dict(zip(a, b))
    out = re.sub(r"\{(\w+)((?:[:!][^{}]*)?)\}", lambda m: "{" + names.get(m[1], m[1]) + m[2] + "}", spanish)
    return out if sorted(fields(out)) == sorted(b) else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--merge", type=Path, help="a JSON {key: Spanish} a translator filled in")
    args = parser.parse_args()
    from gui.i18n import ES
    english = tomllib.loads((ROOT / "pokeldn/app/data/strings.en.toml").read_text(encoding="utf-8"))
    english.update({k: v for k, v in code_keys().items() if k not in english})
    PACK.mkdir(parents=True, exist_ok=True)
    current = tomllib.loads((PACK / "strings.toml").read_text(encoding="utf-8")) if (PACK / "strings.toml").exists() else {}
    if args.merge:
        current.update(json.loads(args.merge.read_text(encoding="utf-8")))
    by_shape = {}
    for key, value in ES.items():
        by_shape.setdefault(shape(key), (key, value))
    strings, todo = {}, {}
    for key, text in english.items():
        if key in current and sorted(fields(current[key])) == sorted(fields(text)):
            strings[key] = current[key]
        elif text in ES and sorted(fields(ES[text])) == sorted(fields(text)):
            strings[key] = ES[text]
        elif (match := by_shape.get(shape(text))) and (spanish := renamed(match[1], match[0], text)):
            strings[key] = spanish
        else:
            todo[key] = text
    messages = {k: v for k, v in ES.items() if not fields(k) and k != v}
    templates = {}
    from pokeldn.app.i18n import _template_fields
    for key, value in ES.items():
        names = fields(key)
        if not names or len(names) > 8 or len(key) > 2048 or len(set(names)) != len(names):
            continue
        try:
            if _template_fields(key, delimited=True) == _template_fields(value) and all(n.isidentifier() for n in names):
                templates[key] = value
        except ValueError:
            continue
    (PACK / "plugin.toml").write_text(PLUGIN, encoding="utf-8")
    write_table(PACK / "strings.toml", strings, "poke-app's Spanish for upstream's keys. scripts/poke_app_spanish_pack.py")
    write_table(PACK / "messages.toml", messages, "Module text, whole. Generated from gui/i18n.py ES.")
    write_table(PACK / "templates.toml", templates, "Module text with fields. Generated from gui/i18n.py ES.")
    write_table(PACK / "terms.toml", TERMS, "Game terms inside module text.")
    TODO.parent.mkdir(exist_ok=True)
    TODO.write_text(json.dumps(todo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(strings)} keys in Spanish, {len(todo)} to translate ({TODO}), {len(messages)} messages, "
          f"{len(templates)} templates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
