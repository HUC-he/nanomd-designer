"""Design panel: parameter form that produces a System."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from nanomd.core.models.system import (
    Box,
    IonSpec,
    MembraneSpec,
    SlitChannel,
    System,
    WaterSpec,
)
from nanomd.gui.i18n import tr


class DesignPanel(QWidget):
    """Parameter form (box size, walls, water, ions, temperature...)."""

    build_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_widgets()
        self._connect()

    def _build_widgets(self) -> None:
        layout = QVBoxLayout(self)
        self._group = QGroupBox()
        form = QFormLayout(self._group)

        self.lx = self._double_spin(10.0, 1000.0, 150.0, 5.0)
        self.ly = self._double_spin(10.0, 1000.0, 40.0, 5.0)
        self.lz = self._double_spin(10.0, 1000.0, 20.0, 5.0)
        self.wall_low = self._double_spin(1.0, 999.0, 5.0, 0.5)
        self.wall_high = self._double_spin(2.0, 1000.0, 15.0, 0.5)
        self.height_label = QLabel()

        self.water = QComboBox()
        self.water.addItem("TIP3P", "tip3p")
        self.water.addItem("SPC/E", "spce")
        self.salt = QComboBox()
        self.salt.addItems(["NaCl", "KCl", "CaCl2"])
        self.conc = self._double_spin(0.05, 5.0, 0.6, 0.05)
        self.temp = self._double_spin(200.0, 500.0, 300.0, 5.0, decimals=0)
        self.seed = QSpinBox()
        self.seed.setRange(1, 2**31 - 1)
        self.seed.setValue(12345)
        self.oxidation = self._double_spin(0.0, 0.5, 0.0, 0.05)
        self.oxidation.setSingleStep(0.05)
        self.group_oh = QCheckBox("-OH")
        self.group_oh.setChecked(True)
        self.group_cooh = QCheckBox("-COOH")
        self.group_nh2 = QCheckBox("-NH2")
        groups_row = QHBoxLayout()
        groups_row.addWidget(self.group_oh)
        groups_row.addWidget(self.group_cooh)
        groups_row.addWidget(self.group_nh2)
        groups_row.addStretch(1)
        self.groups_widget = QWidget()
        self.groups_widget.setLayout(groups_row)

        self._advanced = QGroupBox()
        adv_form = QFormLayout(self._advanced)
        self.target_vel = self._double_spin(0.05, 5.0, 0.5, 0.05)
        self.drive_force = self._double_spin(0.0, 0.1, 0.0005, 0.0001, decimals=5)

        form.addRow(tr("design.lx"), self.lx)
        form.addRow(tr("design.ly"), self.ly)
        form.addRow(tr("design.lz"), self.lz)
        form.addRow(tr("design.lower"), self.wall_low)
        form.addRow(tr("design.upper"), self.wall_high)
        form.addRow(tr("design.height"), self.height_label)
        form.addRow(tr("design.water"), self.water)
        form.addRow(tr("design.salt"), self.salt)
        form.addRow(tr("design.conc"), self.conc)
        form.addRow(tr("design.temp"), self.temp)
        form.addRow(tr("design.seed"), self.seed)
        form.addRow(tr("design.groups"), self.groups_widget)
        form.addRow(tr("design.oxidation"), self.oxidation)

        adv_form.addRow(tr("design.velocity"), self.target_vel)
        adv_form.addRow(tr("design.force"), self.drive_force)

        self.build_button = QPushButton()
        self.build_button.setProperty("primary", True)
        self.build_button.clicked.connect(self.build_requested.emit)

        layout.addWidget(self._group)
        layout.addWidget(self._advanced)
        layout.addWidget(self.build_button)
        layout.addStretch(1)

    def _connect(self) -> None:
        for widget in (self.lx, self.ly, self.lz, self.wall_low, self.wall_high):
            widget.valueChanged.connect(self._update_height)
        self._update_height()

    def _update_height(self) -> None:
        height = self.wall_high.value() - self.wall_low.value()
        self.height_label.setText(f"{height:.1f} Å")

    def _double_spin(
        self,
        lo: float,
        hi: float,
        value: float,
        step: float,
        decimals: int = 1,
    ) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(lo, hi)
        spin.setDecimals(decimals)
        spin.setSingleStep(step)
        spin.setValue(value)
        spin.setKeyboardTracking(False)
        return spin

    def to_system(self) -> System:
        box = Box(self.lx.value(), self.ly.value(), self.lz.value())
        channel = SlitChannel(box, self.wall_low.value(), self.wall_high.value())
        groups = tuple(
            key
            for key, checkbox in (
                ("oh", self.group_oh),
                ("cooh", self.group_cooh),
                ("nh2", self.group_nh2),
            )
            if checkbox.isChecked()
        )
        if not groups:
            raise ValueError("select at least one functional group")
        oxidation = self.oxidation.value()
        return System(
            name="untitled",
            channel=channel,
            water=WaterSpec(model_key=self.water.currentData()),
            ions=IonSpec(salt=self.salt.currentText(), concentration_molar=self.conc.value()),
            membrane=MembraneSpec(
                material="go" if oxidation > 0 else "graphene",
                oxidation_fraction=oxidation,
                functional_groups=groups,
            ),
            temperature_k=self.temp.value(),
            seed=self.seed.value(),
            target_velocity_ang_per_ps=self.target_vel.value(),
            drive_force_kcal_mol_ang=self.drive_force.value(),
        )

    def refresh_texts(self) -> None:
        self._group.setTitle(tr("design.title"))
        self._advanced.setTitle(tr("design.advanced"))
        self.build_button.setText(tr("design.build"))
        form = self._group.layout()
        labels = [
            (0, "design.lx"),
            (1, "design.ly"),
            (2, "design.lz"),
            (3, "design.lower"),
            (4, "design.upper"),
            (5, "design.height"),
            (6, "design.water"),
            (7, "design.salt"),
            (8, "design.conc"),
            (9, "design.temp"),
            (10, "design.seed"),
            (11, "design.groups"),
            (12, "design.oxidation"),
        ]
        for row, key in labels:
            item = form.itemAt(row, QFormLayout.LabelRole)
            if item and item.widget():
                item.widget().setText(tr(key))
        adv_form = self._advanced.layout()
        for row, key in ((0, "design.velocity"), (1, "design.force")):
            item = adv_form.itemAt(row, QFormLayout.LabelRole)
            if item and item.widget():
                item.widget().setText(tr(key))
