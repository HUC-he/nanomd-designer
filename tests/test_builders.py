"""Tests for structure builders (graphene walls, water, ions, full system)."""

import numpy as np
import pytest

from nanomd.core.builders.graphene import AREA_PER_ATOM, build_graphene_walls
from nanomd.core.builders.ions import ion_type_sequence, n_ion_pairs
from nanomd.core.builders.system_builder import build_system
from nanomd.core.builders.water import estimate_n_water, fill_water, make_oxygen_sites
from nanomd.core.models.system import Box, IonSpec, SlitChannel, System, WaterSpec


def make_channel(height: float = 10.0) -> SlitChannel:
    return SlitChannel(Box(150.0, 40.0, 20.0), 5.0, 5.0 + height)


def make_system(seed: int = 123, **kwargs) -> System:
    defaults = dict(
        name="benchmark",
        channel=make_channel(),
        water=WaterSpec(model_key="tip3p"),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
        seed=seed,
    )
    defaults.update(kwargs)
    return System(**defaults)


def test_graphene_walls_geometry() -> None:
    channel = make_channel()
    walls = build_graphene_walls(channel)
    per_wall_expected = channel.box.lx * channel.box.ly / AREA_PER_ATOM
    assert 2 * per_wall_expected * 0.9 < walls.n_atoms < 2 * per_wall_expected * 1.1
    zs = {round(atom.xyz[2], 3) for atom in walls.atoms}
    assert zs == {5.0, 15.0}
    assert walls.total_charge() == pytest.approx(0.0)


def test_graphene_go_oxidation_fraction() -> None:
    walls = build_graphene_walls(make_channel(), oxidation_fraction=0.1, seed=7)
    n_c = sum(1 for a in walls.atoms if a.type_name == "C")
    n_c_oh = sum(1 for a in walls.atoms if a.type_name == "C_OH")
    n_o_g = sum(1 for a in walls.atoms if a.type_name == "O_g")
    n_h_g = sum(1 for a in walls.atoms if a.type_name == "H_g")
    assert 0.08 < n_c_oh / (n_c + n_c_oh) < 0.12
    assert n_o_g == n_c_oh
    assert n_h_g == n_c_oh
    assert walls.total_charge() == pytest.approx(0.0)


def test_graphene_go_all_groups_neutral() -> None:
    walls = build_graphene_walls(
        make_channel(),
        oxidation_fraction=0.3,
        functional_groups=("oh", "cooh", "nh2"),
        seed=11,
    )
    names = {a.type_name for a in walls.atoms}
    assert {"C_OH", "C_carboxyl", "C_NH2"} <= names
    assert walls.total_charge() == pytest.approx(0.0, abs=1e-9)


def test_graphene_go_atoms_inside_box() -> None:
    channel = make_channel()
    walls = build_graphene_walls(
        channel, oxidation_fraction=0.2, functional_groups=("oh", "cooh", "nh2"), seed=3
    )
    box = channel.box
    for atom in walls.atoms:
        assert 0.0 <= atom.xyz[0] < box.lx
        assert 0.0 <= atom.xyz[1] < box.ly
        assert 0.0 <= atom.xyz[2] < box.lz


def test_graphene_go_deterministic() -> None:
    channel = make_channel()
    a = build_graphene_walls(channel, oxidation_fraction=0.2, seed=42)
    b = build_graphene_walls(channel, oxidation_fraction=0.2, seed=42)
    assert a.positions_array() == pytest.approx(b.positions_array())


def test_water_fill_count_and_topology() -> None:
    channel = make_channel()
    target = estimate_n_water(channel)
    water = fill_water(channel, seed=42)
    assert water.n_atoms == 3 * target
    assert len(water.bonds) == 2 * target
    assert len(water.angles) == target
    assert water.total_charge() == pytest.approx(0.0)


def test_water_fill_oxygen_positions() -> None:
    channel = make_channel()
    water = fill_water(channel, seed=7)
    oxygens = np.asarray([atom.xyz for atom in water.atoms if atom.type_name == "O_w"])
    assert np.all(oxygens[:, 2] > channel.lower_wall_z + 1.4)
    assert np.all(oxygens[:, 2] < channel.upper_wall_z - 1.4)
    dists = np.linalg.norm(oxygens[:, None, :] - oxygens[None, :, :], axis=2)
    np.fill_diagonal(dists, np.inf)
    assert dists.min() > 2.4


def test_make_oxygen_sites_exact_count() -> None:
    channel = make_channel()
    assert make_oxygen_sites(channel, 0) == []
    for n in (500, 1400):
        assert len(make_oxygen_sites(channel, n)) == n


def test_ion_type_sequences() -> None:
    assert ion_type_sequence(3, "NaCl", "spec") == ["Na", "Cl"] * 3
    assert ion_type_sequence(2, "CaCl2", "spec") == ["Ca", "Cl", "Cl", "Ca", "Cl", "Cl"]
    with pytest.raises(ValueError):
        ion_type_sequence(1, "NaBr", "spec")


def test_ions_count_and_neutrality() -> None:
    system = make_system(seed=3)
    structure = build_system(system)
    pairs = n_ion_pairs(system.channel, 0.6, "NaCl")
    assert pairs >= 20  # manual constraint: at least 20 ion pairs
    assert structure.total_charge() == pytest.approx(0.0)
    ion_atoms = [a for a in structure.atoms if a.type_name in ("Na+", "Cl-")]
    assert len(ion_atoms) == 2 * pairs


def test_ions_stay_inside_channel() -> None:
    system = make_system(seed=11, ions=IonSpec(salt="KCl", concentration_molar=0.3))
    structure = build_system(system)
    for atom in structure.atoms:
        if atom.type_name in ("K+", "Cl-"):
            lo = system.channel.lower_wall_z + 1.3
            hi = system.channel.upper_wall_z - 1.3
            assert lo < atom.xyz[2] < hi


def test_ions_do_not_overlap_water() -> None:
    system = make_system(seed=5)
    structure = build_system(system)
    positions = structure.positions_array()
    ion_positions = positions[
        np.isin([a.type_name for a in structure.atoms], ["Na+", "Cl-"])
    ]
    o_positions = positions[
        np.isin([a.type_name for a in structure.atoms], ["O_w"])
    ]
    dists = np.linalg.norm(ion_positions[:, None, :] - o_positions[None, :, :], axis=2)
    assert dists.min() > 2.0


def test_build_system_full() -> None:
    system = make_system()
    structure = build_system(system)
    n_water = estimate_n_water(system.channel)
    n_pairs = n_ion_pairs(system.channel, 0.6, "NaCl")
    n_walls = build_graphene_walls(system.channel).n_atoms
    assert structure.n_atoms == n_walls + 3 * n_water + 2 * n_pairs
    assert structure.total_charge() == pytest.approx(0.0, abs=1e-9)


def test_build_system_deterministic() -> None:
    def build_once():
        return build_system(make_system(seed=123)).positions_array()

    assert np.array_equal(build_once(), build_once())


def test_cacl2_stoichiometry() -> None:
    system = make_system(seed=5, ions=IonSpec(salt="CaCl2", concentration_molar=0.3))
    structure = build_system(system)
    assert structure.total_charge() == pytest.approx(0.0)
    n_ca = sum(1 for a in structure.atoms if a.type_name == "Ca2+")
    n_cl = sum(1 for a in structure.atoms if a.type_name == "Cl-")
    assert n_cl == 2 * n_ca
    assert n_ca == n_ion_pairs(system.channel, 0.3, "CaCl2")
