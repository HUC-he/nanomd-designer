"""Salt ion placement (ions share the water packing grid, so the initial
configuration never overlaps)."""

from __future__ import annotations

from nanomd.core.forcefields.library import ION_SETS
from nanomd.core.models.structure import Atom, Structure
from nanomd.core.models.system import SlitChannel

AVOGADRO = 6.02214076e23

SALT_STOICHIOMETRY: dict[str, tuple[str, str, int]] = {
    "NaCl": ("Na", "Cl", 1),
    "KCl": ("K", "Cl", 1),
    "CaCl2": ("Ca", "Cl", 2),
}


def n_ion_pairs(channel: SlitChannel, concentration_molar: float, salt: str = "NaCl") -> int:
    """Ion pairs (formula units) for the geometric channel volume."""
    if salt not in SALT_STOICHIOMETRY:
        raise ValueError(f"unsupported salt: {salt!r}")
    volume_l = channel.channel_volume * 1e-27  # 1 A^3 = 1e-27 L
    return int(round(concentration_molar * volume_l * AVOGADRO))


def ion_type_sequence(n_pairs: int, salt: str, ion_set: str) -> list[str]:
    """Ion-set keys in placement order, e.g. ['Na', 'Cl', 'Na', 'Cl', ...]."""
    if ion_set not in ION_SETS:
        raise ValueError(f"unknown ion set: {ion_set!r}")
    if salt not in SALT_STOICHIOMETRY:
        raise ValueError(f"unsupported salt: {salt!r}")
    cation_key, anion_key, n_anions = SALT_STOICHIOMETRY[salt]
    sequence: list[str] = []
    for _ in range(n_pairs):
        sequence.append(cation_key)
        sequence.extend([anion_key] * n_anions)
    return sequence


def add_ion_atoms(
    structure: Structure,
    positions: list[tuple[float, float, float]],
    ion_keys: list[str],
    ion_set: str,
) -> None:
    """Append ion atoms at the given positions (one per ``ion_keys`` entry)."""
    ions = ION_SETS[ion_set]
    for key, pos in zip(ion_keys, positions, strict=True):
        atom_type = ions[key]
        structure.add_atom(Atom(atom_type.name, atom_type.charge, tuple(pos), molecule=0))
