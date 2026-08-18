"""Regenerate the graphene-slit-nacl example (data, in, preview renders).

Usage (from the repo root):
    python scripts/generate_example.py
"""

from __future__ import annotations

from pathlib import Path

from nanomd.core.builders.system_builder import build_system
from nanomd.core.models.system import Box, IonSpec, SlitChannel, System, WaterSpec
from nanomd.core.writers.data_writer import write_data_file
from nanomd.core.writers.input_writer import write_input_file
from nanomd.gui.scene3d import render_offscreen

OUT = Path(__file__).resolve().parents[1] / "examples" / "graphene-slit-nacl"


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


if __name__ == "__main__":
    main()
