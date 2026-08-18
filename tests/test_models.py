"""Tests for core system data structures."""

import pytest

from nanomd.core.models.system import Box, IonSpec, MembraneSpec, SlitChannel, System


def test_box_rejects_nonpositive() -> None:
    with pytest.raises(ValueError):
        Box(0.0, 10.0, 10.0)


def test_channel_height() -> None:
    channel = SlitChannel(Box(150.0, 40.0, 20.0), lower_wall_z=5.0, upper_wall_z=15.0)
    assert channel.height == pytest.approx(10.0)
    assert channel.channel_volume == pytest.approx(150.0 * 40.0 * 10.0)


def test_channel_rejects_invalid_walls() -> None:
    with pytest.raises(ValueError):
        SlitChannel(Box(150.0, 40.0, 20.0), lower_wall_z=15.0, upper_wall_z=5.0)


def test_membrane_oxidation_fraction_range() -> None:
    with pytest.raises(ValueError):
        MembraneSpec(material="go", oxidation_fraction=1.5)


def test_membrane_rejects_unknown_group() -> None:
    with pytest.raises(ValueError):
        MembraneSpec(functional_groups=("not_a_group",))


def test_default_system_summary() -> None:
    system = System(
        name="benchmark",
        channel=SlitChannel(Box(150.0, 40.0, 20.0), 5.0, 15.0),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
    )
    text = system.summary()
    assert "benchmark" in text
    assert "graphene" in text
    assert "tip3p" in text
    assert "NaCl 0.60 M" in text
