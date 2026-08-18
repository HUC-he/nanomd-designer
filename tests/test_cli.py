"""Smoke tests for the CLI entry point."""

import pytest

from nanomd import __version__
from nanomd.cli import main


def test_version_flag(capsys: pytest.CaptureFixture) -> None:
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert __version__ in out


def test_default_invocation(capsys: pytest.CaptureFixture) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "NanoMD Designer" in out
