"""GUI smoke tests. Skipped automatically when Qt/pyvista are unavailable."""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402

pytest.importorskip("PySide6")
pytest.importorskip("pyvista")
pytest.importorskip("pyvistaqt")


def test_render_offscreen(tmp_path) -> None:
    from nanomd.core.builders.system_builder import build_system
    from nanomd.core.models.system import Box, IonSpec, SlitChannel, System
    from nanomd.gui.scene3d import render_offscreen

    system = System(
        name="smoke",
        channel=SlitChannel(Box(30.0, 15.0, 10.0), 3.0, 7.0),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
        seed=1,
    )
    structure = build_system(system)
    out = render_offscreen(structure, tmp_path / "scene.png", view="top")
    assert out.exists()
    assert out.stat().st_size > 1000


def test_main_window_constructs() -> None:
    if os.environ.get("NANOMD_GUI_TEST") != "1":
        pytest.skip(
            "interactive-window test needs a working OpenGL/X display; "
            "set NANOMD_GUI_TEST=1 on a desktop session to enable"
        )
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    from nanomd.gui.main_window import MainWindow

    window = MainWindow()
    assert window.windowTitle()
    assert window.design.to_system() is not None
    window.close()
    app.processEvents()
