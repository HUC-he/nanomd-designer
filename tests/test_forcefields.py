"""Tests for the force-field parameter library."""

import pytest

from nanomd.core.forcefields.library import (
    FUNCTIONAL_GROUPS,
    GRAPHENE_ATOMS,
    ION_SETS,
    WATER_MODELS,
    all_atom_types,
)


def test_water_models_available() -> None:
    assert {"tip3p", "spce"} <= set(WATER_MODELS)


@pytest.mark.parametrize("key", ["tip3p", "spce"])
def test_water_models_neutral(key: str) -> None:
    assert WATER_MODELS[key].charge_balance == pytest.approx(0.0)


def test_tip3p_matches_project_manual() -> None:
    o = WATER_MODELS["tip3p"].oxygen
    assert (o.charge, o.sigma, o.epsilon) == pytest.approx((-0.834, 3.151, 0.152))


def test_graphene_carbon_matches_manual() -> None:
    c = GRAPHENE_ATOMS["C"]
    assert (c.charge, c.sigma, c.epsilon) == pytest.approx((0.0, 3.550, 0.070))


def test_default_ion_set_has_all_species() -> None:
    assert {"Na", "Cl", "K", "Ca"} <= set(ION_SETS["spec"])


@pytest.mark.parametrize("group_key", ["oh", "cooh", "nh2"])
def test_functional_groups_are_neutral_with_attached_carbon(group_key: str) -> None:
    group = FUNCTIONAL_GROUPS[group_key]
    total = sum(atom.charge for atom in group.atoms) + group.attached_carbon_charge
    assert total == pytest.approx(0.0), f"{group_key} fragment is not charge-neutral"


def test_all_atom_types_have_sources() -> None:
    for atom in all_atom_types().values():
        assert atom.source, f"{atom.name} is missing a source citation"
