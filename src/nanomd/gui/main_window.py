"""Main window: design panel + 3D view + output panel."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)
from pyvistaqt import QtInteractor

from nanomd import __version__
from nanomd.core.builders.system_builder import build_system
from nanomd.core.writers.data_writer import write_data_file
from nanomd.core.writers.input_writer import write_input_file
from nanomd.gui.i18n import set_language, tr
from nanomd.gui.panels.design_panel import DesignPanel
from nanomd.gui.panels.output_panel import OutputPanel
from nanomd.gui.scene3d import add_structure
from nanomd.gui.theme import apply_theme


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._structure = None
        self._system = None
        self._output_folder: Path | None = None
        self._build_ui()
        self.refresh_texts()
        self.rebuild()

    def _build_ui(self) -> None:
        self.design = DesignPanel()
        self.plotter = QtInteractor(self)
        self.output = OutputPanel()

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.plotter.interactor, stretch=3)
        right_layout.addWidget(self.output, stretch=2)

        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self.design)
        split.addWidget(right)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setSizes([320, 780])
        self.setCentralWidget(split)
        self.setMinimumSize(1100, 700)

        self.design.build_requested.connect(self.rebuild)
        self.output.export_requested.connect(self.export_scripts)
        self.output.open_requested.connect(self.open_output_folder)
        self._build_menus()

    def _build_menus(self) -> None:
        menubar = self.menuBar()
        self._menus: dict[str, object] = {}

        file_menu = menubar.addMenu("")
        self._menus["file"] = file_menu
        self._actions = {}
        self._actions["export"] = file_menu.addAction("")
        self._actions["export"].triggered.connect(self.export_scripts)
        file_menu.addSeparator()
        self._actions["quit"] = file_menu.addAction("")
        self._actions["quit"].triggered.connect(self.close)

        lang_menu = menubar.addMenu("")
        self._menus["language"] = lang_menu
        lang_menu.addAction("中文").triggered.connect(lambda: self.set_language("zh"))
        lang_menu.addAction("English").triggered.connect(lambda: self.set_language("en"))

        theme_menu = menubar.addMenu("")
        self._menus["theme"] = theme_menu
        theme_menu.addAction("Deep Channel").triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction("Clear Water").triggered.connect(lambda: self.set_theme("light"))

        help_menu = menubar.addMenu("")
        self._menus["help"] = help_menu
        self._actions["about"] = help_menu.addAction("")
        self._actions["about"].triggered.connect(self._about)

    def refresh_texts(self) -> None:
        self.setWindowTitle(tr("app.title"))
        self._menus["file"].setTitle(tr("menu.file"))
        self._menus["language"].setTitle(tr("menu.language"))
        self._menus["theme"].setTitle(tr("menu.theme"))
        self._menus["help"].setTitle(tr("menu.help"))
        self._actions["export"].setText(tr("action.export"))
        self._actions["quit"].setText(tr("action.quit"))
        self._actions["about"].setText(tr("action.about"))
        self.design.refresh_texts()
        self.output.refresh_texts()

    def set_language(self, lang: str) -> None:
        set_language(lang)
        self.refresh_texts()

    def set_theme(self, name: str) -> None:
        app = QApplication.instance()
        if app is not None:
            apply_theme(app, name)

    def rebuild(self) -> None:
        try:
            system = self.design.to_system()
            structure = build_system(system)
        except Exception as exc:  # noqa: BLE001 - user-facing message
            self._structure = None
            self._system = None
            message = f"{tr('build.error')}: {exc}"
            self.output.set_summary(message)
            self.statusBar().showMessage(message)
            return

        self._system = system
        self._structure = structure
        self.plotter.clear()
        add_structure(self.plotter, structure)
        self.plotter.reset_camera()

        counts = {
            "C": sum(1 for a in structure.atoms if a.type_name == "C"),
            "O_w": sum(1 for a in structure.atoms if a.type_name == "O_w"),
            "ions": sum(
                1
                for a in structure.atoms
                if a.type_name in ("Na+", "Cl-", "K+", "Ca2+")
            ),
        }
        self.output.set_summary(
            f"h = {system.channel.height:.1f} Å · "
            f"{structure.n_atoms} atoms · "
            f"wall C: {counts['C']} · water: {counts['O_w']} · ions: {counts['ions']} · "
            f"charge: {structure.total_charge():.2e}"
        )
        self.statusBar().showMessage(
            f"{structure.n_atoms} atoms · charge {structure.total_charge():.2e}"
        )

    def export_scripts(self) -> None:
        if self._structure is None or self._system is None:
            self.rebuild()
        if self._structure is None or self._system is None:
            QMessageBox.warning(self, tr("app.title"), tr("export.notbuilt"))
            return
        folder = QFileDialog.getExistingDirectory(self, tr("action.export"))
        if not folder:
            return
        target = Path(folder)
        data_path = write_data_file(self._structure, target / "system.data")
        in_path = write_input_file(
            self._system, self._structure, "system.data", target / "in.streaming.lammps"
        )
        self._output_folder = target
        self.output.set_preview(in_path.read_text(encoding="utf-8"))
        QMessageBox.information(
            self,
            tr("app.title"),
            f"{tr('export.ok')}\n{data_path}\n{in_path}",
        )

    def open_output_folder(self) -> None:
        if self._output_folder is None:
            return
        _open_in_explorer(self._output_folder)

    def _about(self) -> None:
        QMessageBox.about(self, tr("app.title"), tr("about.text").format(__version__))


def _open_in_explorer(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(["explorer", str(path)])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
