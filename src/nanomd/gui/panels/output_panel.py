"""Output panel: atom summary, export actions, in-file preview."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from nanomd.gui.i18n import tr


class OutputPanel(QWidget):
    export_requested = Signal()
    open_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_widgets()

    def _build_widgets(self) -> None:
        layout = QVBoxLayout(self)
        self._group = QGroupBox()
        inner = QVBoxLayout(self._group)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        buttons = QHBoxLayout()
        self.export_button = QPushButton()
        self.export_button.setProperty("primary", True)
        self.export_button.clicked.connect(self.export_requested.emit)
        self.open_button = QPushButton()
        self.open_button.clicked.connect(self.open_requested.emit)
        buttons.addWidget(self.export_button)
        buttons.addWidget(self.open_button)
        buttons.addStretch(1)
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMaximumHeight(220)
        inner.addWidget(self.summary)
        inner.addLayout(buttons)
        inner.addWidget(self.preview)
        layout.addWidget(self._group)

    def set_summary(self, text: str) -> None:
        self.summary.setText(text)

    def set_preview(self, text: str) -> None:
        self.preview.setPlainText(text)

    def refresh_texts(self) -> None:
        self._group.setTitle(tr("output.title"))
        self.export_button.setText(tr("action.export"))
        self.open_button.setText(tr("output.open"))
        self.preview.setPlaceholderText(tr("output.preview"))
