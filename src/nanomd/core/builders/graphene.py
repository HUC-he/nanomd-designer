"""Graphene / GO membrane builders."""

from __future__ import annotations

import math

import numpy as np

from nanomd.core.forcefields.library import FUNCTIONAL_GROUPS
from nanomd.core.models.structure import Atom, Structure
from nanomd.core.models.system import SlitChannel

CC_BOND_ANG = 1.42
LATTICE_A = CC_BOND_ANG * math.sqrt(3.0)  # 2.46 A
AREA_PER_ATOM = LATTICE_A**2 * math.sqrt(3.0) / 4.0  # ~2.62 A^2 per carbon


def build_graphene_walls(
    channel: SlitChannel,
    oxidation_fraction: float = 0.0,
    functional_groups: tuple[str, ...] = ("oh",),
    seed: int = 1,
) -> Structure:
    """Build two single-layer graphene sheets at the wall planes.

    The lower/upper sheets lie exactly on ``lower_wall_z`` / ``upper_wall_z``
    and cover the full xy box (x/y periodic). With ``oxidation_fraction > 0``,
    that fraction of surface carbons (per wall) gets a functional group grafted
    into the channel (rough initial geometry; the force field is LJ-only, so
    the groups relax during equilibration).
    """
    if not 0.0 <= oxidation_fraction <= 1.0:
        raise ValueError("oxidation_fraction must be in [0, 1]")
    for key in functional_groups:
        if key not in FUNCTIONAL_GROUPS:
            raise ValueError(f"unknown functional group: {key!r}")
    rng = np.random.default_rng(seed)

    box = channel.box
    structure = Structure(box=box)

    nx = int(math.ceil(box.lx / LATTICE_A)) + 1
    ny = int(math.ceil(box.ly / (LATTICE_A * math.sqrt(3.0) / 2.0))) + 1
    # Hexagonal lattice: a1 = a*(1,0), a2 = a*(1/2, sqrt(3)/2),
    # basis A = (0,0), B = (a/2, a/(2*sqrt(3))) -> C-C distance 1.42 A.
    basis = ((0.0, 0.0), (LATTICE_A / 2.0, LATTICE_A / (2.0 * math.sqrt(3.0))))

    wall_zs = (channel.lower_wall_z, channel.upper_wall_z)
    for z in wall_zs:
        for ix in range(nx):
            for iy in range(ny):
                for bx, by in basis:
                    x = ix * LATTICE_A + iy * LATTICE_A * 0.5 + bx
                    y = iy * LATTICE_A * math.sqrt(3.0) / 2.0 + by
                    if 0.0 <= x < box.lx and 0.0 <= y < box.ly:
                        structure.add_atom(Atom("C", 0.0, (x, y, z), molecule=0))

    if oxidation_fraction > 0.0:
        _functionalize(
            structure,
            channel,
            wall_zs,
            oxidation_fraction,
            functional_groups,
            rng,
        )
    return structure


def _functionalize(
    structure: Structure,
    channel: SlitChannel,
    wall_zs: tuple[float, float],
    oxidation_fraction: float,
    groups: tuple[str, ...],
    rng: np.random.Generator,
) -> None:
    """Graft functional groups onto a random subset of wall carbons."""
    for wall_z in wall_zs:
        direction = 1.0 if wall_z < 0.5 * (channel.lower_wall_z + channel.upper_wall_z) else -1.0
        wall_indices = [
            i
            for i, atom in enumerate(structure.atoms)
            if atom.type_name in ("C", "C_OH", "C_NH2") and abs(atom.xyz[2] - wall_z) < 1e-6
        ]
        n_mod = int(round(len(wall_indices) * oxidation_fraction))
        chosen = rng.choice(wall_indices, size=n_mod, replace=False)
        for carbon_idx in chosen:
            group_key = str(rng.choice(groups))
            _attach_group(structure, carbon_idx, group_key, direction, rng)


def _attach_group(
    structure: Structure,
    carbon_idx: int,
    group_key: str,
    direction: float,
    rng: np.random.Generator,
) -> None:
    """Attach one functional group, oriented into the channel along z."""
    group = FUNCTIONAL_GROUPS[group_key]
    carbon = structure.atoms[carbon_idx]
    cx, cy, cz = carbon.xyz
    charges = {atom.name: atom.charge for atom in group.atoms}
    carbon.charge = group.attached_carbon_charge

    if group_key == "oh":
        carbon.type_name = "C_OH"
        positions = [
            ("O_g", (cx, cy, cz + direction * 1.36)),
            ("H_g", (cx, cy, cz + direction * (1.36 + 0.96))),
        ]

    elif group_key == "cooh":
        # graphene C keeps charge 0.0 (fragment is neutral)
        cc = (cx, cy, cz + direction * 1.5)
        o_carbonyl = (cc[0], cc[1], cc[2] + direction * 1.23)
        perp = _random_xy_unit(rng)
        o_hydroxyl = (cc[0] + perp[0] * 1.36, cc[1] + perp[1] * 1.36, cc[2])
        h = (o_hydroxyl[0] + perp[0] * 0.96, o_hydroxyl[1] + perp[1] * 0.96, o_hydroxyl[2])
        positions = [
            ("C_carboxyl", cc),
            ("O_c(=O)", o_carbonyl),
            ("O_c(-OH)", o_hydroxyl),
            ("H_c", h),
        ]

    elif group_key == "nh2":
        carbon.type_name = "C_NH2"
        n = (cx, cy, cz + direction * 1.47)
        u = _random_xy_unit(rng)
        v = (
            u[0] * math.cos(1.884) - u[1] * math.sin(1.884),
            u[0] * math.sin(1.884) + u[1] * math.cos(1.884),
        )
        h1 = (n[0] + u[0] * 1.01, n[1] + u[1] * 1.01, n[2])
        h2 = (n[0] + v[0] * 1.01, n[1] + v[1] * 1.01, n[2])
        positions = [
            ("N_amine", n),
            ("H_amine", h1),
            ("H_amine", h2),
        ]

    for name, pos in positions:
        structure.add_atom(Atom(name, charges[name], _clamp(pos, structure.box), molecule=0))


def _random_xy_unit(rng: np.random.Generator) -> tuple[float, float]:
    angle = rng.uniform(0.0, 2.0 * math.pi)
    return (math.cos(angle), math.sin(angle))


def _clamp(
    pos: tuple[float, float, float], box
) -> tuple[float, float, float]:
    """Keep grafted atoms inside the periodic box (edge carbons may point out)."""
    return (
        min(max(pos[0], 0.0), box.lx - 1e-9),
        min(max(pos[1], 0.0), box.ly - 1e-9),
        min(max(pos[2], 0.0), box.lz - 1e-9),
    )
