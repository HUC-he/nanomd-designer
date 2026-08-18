"""Water filling (TIP3P / SPC-E) for the channel fluid region."""

from __future__ import annotations

import math

import numpy as np

from nanomd.core.forcefields.library import WATER_MODELS
from nanomd.core.models.structure import Atom, Structure
from nanomd.core.models.system import SlitChannel

AVOGADRO = 6.02214076e23
WATER_MOLAR_MASS = 18.01528  # g/mol
GRID_SPACING = 2.85  # A, initial O-O spacing on the packing grid


def estimate_n_water(
    channel: SlitChannel,
    density_g_cm3: float = 1.0,
    wall_margin: float = 1.5,
) -> int:
    """Water molecules for a target density in the accessible fluid region
    (channel height minus wall margins)."""
    fluid_volume = (
        max(channel.height - 2.0 * wall_margin, 0.0) * channel.box.lx * channel.box.ly
    )
    molecules_per_ang3 = density_g_cm3 * AVOGADRO / WATER_MOLAR_MASS / 1e24
    return int(round(fluid_volume * molecules_per_ang3))


def make_oxygen_sites(
    channel: SlitChannel,
    n_sites: int,
    wall_margin: float = 1.5,
    spacing: float = GRID_SPACING,
    rng: np.random.Generator | None = None,
) -> list[tuple[float, float, float]]:
    """Exactly ``n_sites`` oxygen positions inside the fluid region.

    Sites are drawn from a jittered simple-cubic grid; if the grid has too
    few cells, the axis with the largest spacing is subdivided. Both water
    and ions share these sites so nothing overlaps in the initial config.
    """
    if n_sites <= 0:
        return []
    rng = rng if rng is not None else np.random.default_rng(0)

    box = channel.box
    z_lo = channel.lower_wall_z + wall_margin
    z_hi = channel.upper_wall_z - wall_margin
    if z_hi <= z_lo:
        raise ValueError("channel too narrow for the requested wall margin")
    span_z = z_hi - z_lo

    nx = max(1, int(math.floor(box.lx / spacing)))
    ny = max(1, int(math.floor(box.ly / spacing)))
    nz = max(1, int(math.floor(span_z / spacing)))
    while nx * ny * nz < n_sites:
        spacings = (box.lx / nx, box.ly / ny, span_z / nz)
        axis = int(np.argmax(spacings))
        if axis == 0:
            nx += 1
        elif axis == 1:
            ny += 1
        else:
            nz += 1

    sx, sy, sz = box.lx / nx, box.ly / ny, span_z / nz
    sites = [
        ((ix + 0.5) * sx, (iy + 0.5) * sy, z_lo + (iz + 0.5) * sz)
        for ix in range(nx)
        for iy in range(ny)
        for iz in range(nz)
    ]
    if len(sites) > n_sites:
        chosen = rng.choice(len(sites), size=n_sites, replace=False)
        sites = [sites[i] for i in chosen]

    jitter = rng.uniform(-0.1, 0.1, size=(len(sites), 3))
    return [
        tuple(np.asarray(site, dtype=float) + dpos)
        for site, dpos in zip(sites, jitter, strict=True)
    ]


def _random_unit_vectors(rng: np.random.Generator, n: int) -> np.ndarray:
    """(n, 3) uniformly random unit vectors."""
    v = rng.normal(size=(n, 3))
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    return v / np.maximum(norms, 1e-12)


def add_water_molecules(
    structure: Structure,
    sites: list[tuple[float, float, float]],
    model_key: str,
    rng: np.random.Generator | None = None,
    start_mol_id: int = 1,
) -> None:
    """Add one rigid water molecule per site (O at site, H's oriented
    randomly with the correct bond length / angle)."""
    if model_key not in WATER_MODELS:
        raise ValueError(f"unknown water model: {model_key!r}")
    model = WATER_MODELS[model_key]
    rng = rng if rng is not None else np.random.default_rng(0)
    n = len(sites)
    if n == 0:
        return

    u = _random_unit_vectors(rng, n)
    w = _random_unit_vectors(rng, n)
    w = w - np.einsum("ij,ij->i", w, u)[:, None] * u
    w /= np.maximum(np.linalg.norm(w, axis=1, keepdims=True), 1e-12)

    bond = model.oh_bond_ang
    theta = math.radians(model.hoh_angle_deg)
    o_charge = model.oxygen.charge
    h_charge = model.hydrogen.charge
    o_name = model.oxygen.name
    h_name = model.hydrogen.name

    for mol_id, (site, ui, wi) in enumerate(
        zip(sites, u, w, strict=True), start=start_mol_id
    ):
        o = tuple(np.asarray(site, dtype=float))
        o_idx = structure.add_atom(Atom(o_name, o_charge, o, molecule=mol_id))
        h1 = tuple(np.asarray(o) + bond * ui)
        h2 = tuple(np.asarray(o) + bond * (math.cos(theta) * ui + math.sin(theta) * wi))
        h1_idx = structure.add_atom(Atom(h_name, h_charge, h1, molecule=mol_id))
        h2_idx = structure.add_atom(Atom(h_name, h_charge, h2, molecule=mol_id))
        structure.add_bond(o_idx, h1_idx)
        structure.add_bond(o_idx, h2_idx)
        structure.add_angle(h1_idx, o_idx, h2_idx)


def fill_water(
    channel: SlitChannel,
    model_key: str = "tip3p",
    density_g_cm3: float = 1.0,
    n_molecules: int | None = None,
    wall_margin: float = 1.5,
    seed: int = 1,
) -> Structure:
    """Standalone water fill (used directly by tests and the GUI preview)."""
    rng = np.random.default_rng(seed)
    target = (
        n_molecules
        if n_molecules is not None
        else estimate_n_water(channel, density_g_cm3, wall_margin)
    )
    structure = Structure(box=channel.box)
    sites = make_oxygen_sites(channel, target, wall_margin, GRID_SPACING, rng)
    add_water_molecules(structure, sites, model_key, rng, start_mol_id=1)
    return structure
