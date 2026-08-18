"""NanoMD Designer GUI entry point."""

from __future__ import annotations

import sys


def main() -> int:
    from PySide6.QtWidgets import QApplication

    from nanomd import __version__
    from nanomd.gui.main_window import MainWindow
    from nanomd.gui.theme import apply_theme

    app = QApplication(sys.argv)
    app.setApplicationName("NanoMD Designer")
    app.setApplicationVersion(__version__)
    apply_theme(app, "dark")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
