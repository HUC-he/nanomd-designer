"""LAMMPS data file writer (``atom_style full``)."""

from __future__ import annotations

from pathlib import Path

from nanomd.core.forcefields.library import ELEMENT_MASS, all_atom_types
from nanomd.core.models.structure import Structure


def write_data_file(
    structure: Structure,
    path: str | Path,
    title: str = "NanoMD Designer",
) -> Path:
    """Write a LAMMPS data file and return the output path."""
    path = Path(path)
    types = structure.type_names()
    type_id = {name: i + 1 for i, name in enumerate(types)}
    library = all_atom_types()
    masses = {name: ELEMENT_MASS[library[name].element] for name in types}

    lines: list[str] = [
        f"LAMMPS data file from {title}",
        "",
        f"{structure.n_atoms} atoms",
        f"{len(structure.bonds)} bonds",
        f"{len(structure.angles)} angles",
        "",
        f"{len(types)} atom types",
        "1 bond types",
        "1 angle types",
        "",
        f"0 {structure.box.lx:.6f} xlo xhi",
        f"0 {structure.box.ly:.6f} ylo yhi",
        f"0 {structure.box.lz:.6f} zlo zhi",
        "",
        "Masses",
        "",
    ]
    for name in types:
        lines.append(f"{type_id[name]} {masses[name]:.3f}")

    lines += ["", "Atoms  # full", ""]
    for i, atom in enumerate(structure.atoms, start=1):
        x, y, z = atom.xyz
        lines.append(
            f"{i} {atom.molecule} {type_id[atom.type_name]} "
            f"{atom.charge:.6f} {x:.6f} {y:.6f} {z:.6f}"
        )

    if structure.bonds:
        lines += ["", "Bonds", ""]
        for i, (a, b) in enumerate(structure.bonds, start=1):
            lines.append(f"{i} 1 {a + 1} {b + 1}")
    if structure.angles:
        lines += ["", "Angles", ""]
        for i, (a, b, c) in enumerate(structure.angles, start=1):
            lines.append(f"{i} 1 {a + 1} {b + 1} {c + 1}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
