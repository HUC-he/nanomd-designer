"""Tests for the lightweight zh/en translation layer."""

from nanomd.gui.i18n import set_language, tr


def test_zh_default() -> None:
    set_language("zh")
    assert tr("design.title") == "体系设计"


def test_en_translation() -> None:
    set_language("en")
    assert tr("design.title") == "System Design"
    assert tr("design.water") == "Water model"


def test_missing_key_returns_key() -> None:
    set_language("zh")
    assert tr("no.such.key") == "no.such.key"


def test_invalid_language_rejected() -> None:
    try:
        set_language("fr")
    except ValueError:
        return
    raise AssertionError("set_language should reject unsupported languages")
