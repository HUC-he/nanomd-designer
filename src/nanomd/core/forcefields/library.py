"""Force-field parameter library v1.

All values are in LAMMPS *real* units: charge in e, sigma in Angstrom,
epsilon in kcal/mol. Every entry carries its literature source so the
parameter set stays auditable.
"""

from __future__ import annotations

from dataclasses import dataclass

SOURCE_SPEC = "碳基水伏 MD 技术规格手册 (project spec)"
SOURCE_TIP3P = "Jorgensen et al., J. Chem. Phys. 79, 926 (1983)"
SOURCE_SPCE = "Berendsen et al., J. Phys. Chem. 91, 6269 (1987)"
SOURCE_OPLSAA = "Jorgensen et al., J. Am. Chem. Soc. 118, 11225 (1996)"
SOURCE_AQVIST = "Aqvist, J. Phys. Chem. 94, 8021 (1990)"
SOURCE_OPLSAA_2024 = "OPLS-AA 2024 (moltemplate, J. Phys. Chem. B 2023 supplement)"

ELEMENT_MASS: dict[str, float] = {
    "C": 12.011,
    "H": 1.008,
    "O": 15.999,
    "N": 14.007,
    "Na": 22.990,
    "Cl": 35.450,
    "K": 39.098,
    "Ca": 40.078,
}


@dataclass(frozen=True)
class AtomType:
    """LJ + charge parameters for one atom type."""

    name: str
    element: str
    charge: float
    sigma: float
    epsilon: float
    source: str
    note: str = ""


@dataclass(frozen=True)
class WaterModel:
    """Rigid water model (TIP3P / SPC/E)."""

    key: str
    display_name: str
    oxygen: AtomType
    hydrogen: AtomType
    oh_bond_ang: float
    hoh_angle_deg: float
    source: str

    @property
    def charge_balance(self) -> float:
        return self.oxygen.charge + 2.0 * self.hydrogen.charge


@dataclass(frozen=True)
class FunctionalGroup:
    """A grafted functional group and the charge it puts on the carbon it
    attaches to (keeps the whole fragment charge-neutral)."""

    key: str
    name: str
    atoms: tuple[AtomType, ...]
    attached_carbon_charge: float
    source: str


WATER_MODELS: dict[str, WaterModel] = {
    "tip3p": WaterModel(
        key="tip3p",
        display_name="TIP3P",
        oxygen=AtomType("O_w", "O", -0.834, 3.151, 0.152, SOURCE_TIP3P),
        hydrogen=AtomType("H_w", "H", 0.417, 1.0, 0.0, SOURCE_TIP3P),
        oh_bond_ang=0.9572,
        hoh_angle_deg=104.52,
        source=SOURCE_TIP3P,
    ),
    "spce": WaterModel(
        key="spce",
        display_name="SPC/E",
        oxygen=AtomType("O_w", "O", -0.8476, 3.166, 0.155, SOURCE_SPCE),
        hydrogen=AtomType("H_w", "H", 0.4238, 1.0, 0.0, SOURCE_SPCE),
        oh_bond_ang=1.0,
        hoh_angle_deg=109.47,
        source=SOURCE_SPCE,
    ),
}


GRAPHENE_ATOMS: dict[str, AtomType] = {
    "C": AtomType("C", "C", 0.0, 3.550, 0.070, SOURCE_SPEC),
    "C_OH": AtomType("C_OH", "C", 0.150, 3.550, 0.070, SOURCE_SPEC),
}


# Ion parameter sets. The default "spec" set follows the project manual for
# Na+/Cl- and the same-family OPLS values for K+, plus Aqvist 1990 for Ca2+.
ION_SETS: dict[str, dict[str, AtomType]] = {
    "spec": {
        "Na": AtomType("Na+", "Na", 1.0, 4.070, 0.001, SOURCE_SPEC),
        "Cl": AtomType("Cl-", "Cl", -1.0, 4.020, 0.710, SOURCE_SPEC),
        "K": AtomType(
            "K+",
            "K",
            1.0,
            5.17,
            0.0005,
            SOURCE_OPLSAA_2024,
            "same family as manual Na+; alternative Aqvist 4.935 / 0.000328",
        ),
        "Ca": AtomType("Ca2+", "Ca", 2.0, 2.412, 0.450, SOURCE_AQVIST),
    },
}


FUNCTIONAL_GROUPS: dict[str, FunctionalGroup] = {
    "oh": FunctionalGroup(
        key="oh",
        name="-OH (hydroxyl)",
        atoms=(
            AtomType("O_g", "O", -0.585, 3.070, 0.170, SOURCE_SPEC),
            AtomType("H_g", "H", 0.435, 1.0, 0.0, SOURCE_SPEC),
        ),
        attached_carbon_charge=0.150,
        source=SOURCE_SPEC,
    ),
    "cooh": FunctionalGroup(
        key="cooh",
        name="-COOH (carboxyl)",
        atoms=(
            AtomType("C_carboxyl", "C", 0.520, 3.750, 0.105, SOURCE_OPLSAA_2024),
            AtomType("O_c(=O)", "O", -0.440, 2.960, 0.210, SOURCE_OPLSAA_2024),
            AtomType("O_c(-OH)", "O", -0.530, 3.000, 0.170, SOURCE_OPLSAA_2024),
            AtomType("H_c", "H", 0.450, 1.0, 0.0, SOURCE_OPLSAA_2024),
        ),
        attached_carbon_charge=0.0,
        source=SOURCE_OPLSAA_2024,
    ),
    "nh2": FunctionalGroup(
        key="nh2",
        name="-NH2 (amine)",
        atoms=(
            AtomType("N_amine", "N", -0.900, 3.300, 0.170, SOURCE_OPLSAA_2024),
            AtomType("H_amine", "H", 0.360, 1.0, 0.0, SOURCE_OPLSAA_2024),
            AtomType("H_amine", "H", 0.360, 1.0, 0.0, SOURCE_OPLSAA_2024),
        ),
        attached_carbon_charge=0.180,
        source=SOURCE_OPLSAA_2024,
    ),
}


def all_atom_types(prefer_water: str | None = None) -> dict[str, AtomType]:
    """Flatten every atom type into one name -> AtomType map.

    Water oxygens/hydrogens share type names across models (``O_w``/``H_w``),
    so ``prefer_water`` selects which model's values win.
    """
    out: dict[str, AtomType] = dict(GRAPHENE_ATOMS)
    if prefer_water is not None:
        model = WATER_MODELS[prefer_water]
        out[model.oxygen.name] = model.oxygen
        out[model.hydrogen.name] = model.hydrogen
    else:
        for model in WATER_MODELS.values():
            out.setdefault(model.oxygen.name, model.oxygen)
            out.setdefault(model.hydrogen.name, model.hydrogen)
    for ion_set in ION_SETS.values():
        for atom in ion_set.values():
            out[atom.name] = atom
    for group in FUNCTIONAL_GROUPS.values():
        for atom in group.atoms:
            out[atom.name] = atom
    return out
