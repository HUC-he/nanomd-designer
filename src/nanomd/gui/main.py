"""Minimal GUI entry point (M0 placeholder).

The full user interface arrives in M1. This entry point only verifies that
the Qt stack is importable and shows a short message.
"""

from __future__ import annotations


def main() -> int:
    from nanomd import __version__

    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
    except ImportError:
        print(
            "NanoMD Designer GUI requires PySide6. Install it with:\n"
            '  pip install -e ".[gui]"'
        )
        return 1

    app = QApplication([])
    QMessageBox.information(
        None,
        "NanoMD Designer",
        f"NanoMD Designer {__version__}\n\n"
        "The GUI arrives in M1 (Windows + WSL bridge).\nStay tuned!",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
