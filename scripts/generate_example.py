"""Regenerate the graphene-slit-nacl example (data, in, preview renders).

Usage (from the repo root):
    python scripts/generate_example.py
"""

from __future__ import annotations

from pathlib import Path

from nanomd.core.builders.system_builder import build_system
from nanomd.core.models.system import (
    Box,
    IonSpec,
    MembraneSpec,
    SlitChannel,
    System,
    WaterSpec,
)
from nanomd.core.writers.data_writer import write_data_file
from nanomd.core.writers.input_writer import write_input_file
from nanomd.gui.scene3d import render_offscreen

OUT = Path(__file__).resolve().parents[1] / "examples" / "graphene-slit-nacl"
GO_OUT = Path(__file__).resolve().parents[1] / "examples" / "go-oh-10-slit"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    system = System(
        name="graphene-slit-nacl",
        channel=SlitChannel(Box(150.0, 40.0, 20.0), 5.0, 15.0),
        water=WaterSpec(model_key="tip3p"),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
        seed=12345,
    )
    structure = build_system(system)
    write_data_file(structure, OUT / "system.data")
    write_input_file(system, structure, "system.data", OUT / "in.streaming.lammps")
    render_offscreen(structure, OUT / "preview_3d.png", view="isometric")
    render_offscreen(structure, OUT / "preview_top.png", view="top")
    print(f"example regenerated: {structure.n_atoms} atoms in {OUT}")

    GO_OUT.mkdir(parents=True, exist_ok=True)
    go_system = System(
        name="go-oh-10-slit",
        channel=SlitChannel(Box(150.0, 40.0, 20.0), 5.0, 15.0),
        membrane=MembraneSpec(
            material="go", oxidation_fraction=0.1, functional_groups=("oh",)
        ),
        water=WaterSpec(model_key="tip3p"),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
        seed=12345,
    )
    go_structure = build_system(go_system)
    write_data_file(go_structure, GO_OUT / "system.data")
    write_input_file(go_system, go_structure, "system.data", GO_OUT / "in.streaming.lammps")
    render_offscreen(go_structure, GO_OUT / "preview_3d.png", view="isometric")
    print(f"GO example generated: {go_structure.n_atoms} atoms in {GO_OUT}")


if __name__ == "__main__":
    main()
