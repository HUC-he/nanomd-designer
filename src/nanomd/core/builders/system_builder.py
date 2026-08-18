"""Assemble a complete System into a Structure (walls + water + ions)."""

from __future__ import annotations

import numpy as np

from nanomd.core.builders.graphene import build_graphene_walls
from nanomd.core.builders.ions import add_ion_atoms, ion_type_sequence, n_ion_pairs
from nanomd.core.builders.water import (
    add_water_molecules,
    estimate_n_water,
    make_oxygen_sites,
)
from nanomd.core.models.structure import Structure
from nanomd.core.models.system import System

WALL_MARGIN = 1.5  # A, oxygen/ion distance from each wall plane


def build_system(system: System) -> Structure:
    """Build the full atomistic structure described by ``system``.

    Water oxygens and ions share one packing grid: ions claim random grid
    sites first, water fills the rest, so the initial configuration has no
    overlaps even in narrow (1 nm) channels.
    """
    if system.membrane.material not in ("graphene", "go"):
        raise ValueError(f"unsupported membrane material: {system.membrane.material!r}")

    walls = build_graphene_walls(
        system.channel,
        oxidation_fraction=system.membrane.oxidation_fraction,
        seed=system.seed,
    )
    merged = Structure(box=system.channel.box)
    for atom in walls.atoms:
        merged.add_atom(atom)

    ion_keys: list[str] = []
    if system.ions is not None:
        pairs = n_ion_pairs(
            system.channel, system.ions.concentration_molar, system.ions.salt
        )
        ion_keys = ion_type_sequence(pairs, system.ions.salt, system.ions.ion_set)

    rng = np.random.default_rng(system.seed)
    n_water = system.water.n_molecules or estimate_n_water(
        system.channel, system.water.density_g_cm3
    )
    sites = make_oxygen_sites(
        system.channel, n_water + len(ion_keys), WALL_MARGIN, rng=rng
    )

    if ion_keys:
        order = rng.permutation(len(sites))[: len(ion_keys)]
        ion_positions = [sites[i] for i in order]
        chosen = set(order.tolist())
        water_sites = [site for i, site in enumerate(sites) if i not in chosen]
    else:
        ion_positions = []
        water_sites = sites

    add_water_molecules(merged, water_sites, system.water.model_key, rng, start_mol_id=1)
    if ion_keys:
        add_ion_atoms(merged, ion_positions, ion_keys, system.ions.ion_set)
    return merged
