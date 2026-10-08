import pytest


@pytest.fixture(autouse=True)
def _english_interface():
    """The tests assert the app's English texts; poke-app's interface starts in Spanish (gui.i18n)."""
    from gui import i18n
    previous = i18n.language()
    i18n.set_language("en")
    yield
    i18n.set_language(previous)
