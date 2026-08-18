"""In-memory representation of a generated atomic structure."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from nanomd.core.models.system import Box


@dataclass
class Atom:
    """One atom. ``type_name`` is the force-field library key used to look up
    its parameters when writing LAMMPS data files."""

    type_name: str
    charge: float
    xyz: tuple[float, float, float]
    molecule: int = 0


@dataclass
class Structure:
    """Atoms plus bond/angle topology (bonds are needed for rigid water/SHAKE)."""

    box: Box
    atoms: list[Atom] = field(default_factory=list)
    bonds: list[tuple[int, int]] = field(default_factory=list)
    angles: list[tuple[int, int, int]] = field(default_factory=list)

    def add_atom(self, atom: Atom) -> int:
        self.atoms.append(atom)
        return len(self.atoms) - 1

    def add_bond(self, i: int, j: int) -> None:
        self.bonds.append((i, j))

    def add_angle(self, i: int, j: int, k: int) -> None:
        self.angles.append((i, j, k))

    @property
    def n_atoms(self) -> int:
        return len(self.atoms)

    def positions_array(self) -> np.ndarray:
        """(n_atoms, 3) float array of positions."""
        return np.asarray([atom.xyz for atom in self.atoms], dtype=float)

    def total_charge(self) -> float:
        return sum(atom.charge for atom in self.atoms)

    def type_names(self) -> list[str]:
        """Unique atom type names in order of first appearance."""
        seen: dict[str, None] = {}
        for atom in self.atoms:
            seen.setdefault(atom.type_name, None)
        return list(seen)
