"""Graphene / GO membrane builders.

M1 builds pristine graphene sheets; GO functionalization lands in M2.
"""

from __future__ import annotations

import math

from nanomd.core.models.structure import Atom, Structure
from nanomd.core.models.system import SlitChannel

CC_BOND_ANG = 1.42
LATTICE_A = CC_BOND_ANG * math.sqrt(3.0)  # 2.46 A
AREA_PER_ATOM = LATTICE_A**2 * math.sqrt(3.0) / 4.0  # ~2.62 A^2 per carbon


def build_graphene_walls(
    channel: SlitChannel,
    oxidation_fraction: float = 0.0,
    seed: int = 1,
) -> Structure:
    """Build two pristine single-layer graphene sheets at the wall planes.

    The lower/upper sheets lie exactly on ``lower_wall_z`` / ``upper_wall_z``
    and cover the full xy box (x/y periodic).
    """
    if oxidation_fraction > 0.0:
        raise NotImplementedError(
            "GO functionalization arrives in M2; use pristine graphene for M1."
        )
    del seed  # lattice is deterministic; seed is used by oxidation in M2

    box = channel.box
    structure = Structure(box=box)

    nx = int(math.ceil(box.lx / LATTICE_A)) + 1
    ny = int(math.ceil(box.ly / (LATTICE_A * math.sqrt(3.0) / 2.0))) + 1
    # Hexagonal lattice: a1 = a*(1,0), a2 = a*(1/2, sqrt(3)/2),
    # basis A = (0,0), B = (a/2, a/(2*sqrt(3))) -> C-C distance 1.42 A.
    basis = ((0.0, 0.0), (LATTICE_A / 2.0, LATTICE_A / (2.0 * math.sqrt(3.0))))

    for z in (channel.lower_wall_z, channel.upper_wall_z):
        for ix in range(nx):
            for iy in range(ny):
                for bx, by in basis:
                    x = ix * LATTICE_A + iy * LATTICE_A * 0.5 + bx
                    y = iy * LATTICE_A * math.sqrt(3.0) / 2.0 + by
                    if 0.0 <= x < box.lx and 0.0 <= y < box.ly:
                        structure.add_atom(Atom("C", 0.0, (x, y, z), molecule=0))
    return structure
