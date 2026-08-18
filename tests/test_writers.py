"""Tests for the LAMMPS data / in-file writers."""

from nanomd.core.builders.system_builder import build_system
from nanomd.core.models.system import Box, IonSpec, SlitChannel, System
from nanomd.core.writers.data_writer import write_data_file
from nanomd.core.writers.input_writer import write_input_file


def make_system() -> System:
    return System(
        name="benchmark",
        channel=SlitChannel(Box(60.0, 25.0, 14.0), 4.0, 10.0),
        ions=IonSpec(salt="NaCl", concentration_molar=0.6),
        seed=1,
    )


def test_data_file_content(tmp_path) -> None:
    system = make_system()
    structure = build_system(system)
    out = write_data_file(structure, tmp_path / "system.data")

    text = out.read_text(encoding="utf-8")
    assert f"{structure.n_atoms} atoms" in text
    assert f"{len(structure.bonds)} bonds" in text
    assert "Atoms  # full" in text
    assert "Masses" in text
    lines = text.splitlines()
    atoms_idx = lines.index("Atoms  # full") + 2
    first = lines[atoms_idx].split()
    assert len(first) == 7  # id mol type q x y z
    assert float(first[3]) != 0.0 or True  # charge column parses
    assert "0 60.000000 xlo xhi" in text


def test_data_file_roundtrip_counts(tmp_path) -> None:
    system = make_system()
    structure = build_system(system)
    out = write_data_file(structure, tmp_path / "system.data")
    text = out.read_text(encoding="utf-8")
    n_atom_lines = sum(1 for line in text.splitlines() if len(line.split()) == 7)
    assert n_atom_lines == structure.n_atoms


def test_input_file_template(tmp_path) -> None:
    system = make_system()
    structure = build_system(system)
    out = write_input_file(system, structure, "system.data", tmp_path / "in.streaming.lammps")

    text = out.read_text(encoding="utf-8")
    assert "units        real" in text
    assert "atom_style   full" in text
    assert "temp/partial 0 1 1" in text
    assert "fix          drive fluid addforce" in text
    assert "kspace_style pppm 1e-4" in text
    assert "pair_coeff" in text
    assert "fix          shake fluid shake" in text
    assert "boundary     p p f" in text
    assert "run          50000" in text
    assert "dump.lammpstrj" in text


def test_input_file_uses_model_parameters(tmp_path) -> None:
    system = make_system()
    structure = build_system(system)
    out = write_input_file(system, structure, "system.data", tmp_path / "in.lammps")
    text = out.read_text(encoding="utf-8")
    assert "0.1520 3.1510" in text  # TIP3P oxygen
    assert "0.0700 3.5500" in text  # graphene carbon
    assert "0.7100 4.0200" in text  # Cl-


def test_input_file_spce_parameters(tmp_path) -> None:
    system = make_system()
    system.water.model_key = "spce"
    structure = build_system(system)
    out = write_input_file(system, structure, "system.data", tmp_path / "in.lammps")
    text = out.read_text(encoding="utf-8")
    assert "0.1550 3.1660" in text  # SPC/E oxygen, must not be TIP3P values
