# NanoMD Designer

[![CI](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml/badge.svg)](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Design nanochannel molecular-dynamics systems on Windows, generate production-ready LAMMPS scripts, and run them anywhere — no terminal, no Linux, no scripting.**

> 中文版：[README.zh-CN.md](README.zh-CN.md) · 纳米流体 / 电化学界面 / 石墨烯通道 / 流致电势 分子动力学建模工具

NanoMD Designer is an open-source, bilingual (中文 / EN) desktop GUI for building and setting up molecular dynamics (MD) simulations of **nanofluidics and electrochemical interfaces** with [LAMMPS](https://www.lammps.org). It is made for materials / chemistry / physics researchers on Windows who want to focus on science instead of hand-writing LAMMPS input scripts.

**Keywords:** molecular dynamics · LAMMPS · nanofluidics · graphene · graphene oxide · nanochannel · streaming potential · streaming current · electrokinetics · electrochemical interface · electrical double layer · water desalination · ion transport · hydrovoltaic · MD modeling · scientific computing · Python GUI · open source

## Who is it for? (Applicable research fields)

| Field | What NanoMD Designer helps with |
|---|---|
| **Nanofluidics** | Building water-filled graphene / GO slit channels; studying flow, slip length, and streaming current / potential under pressure-driven flow |
| **Electrokinetics & electrochemical interfaces** | Electrical double layers, ion transport, and surface-charge effects at charged carbon interfaces |
| **Water desalination & membrane science** | Graphene / GO nanochannel models for water permeation and ion-rejection studies |
| **Energy harvesting (hydrovoltaic)** | Flow-induced streaming potential in carbon nanochannels for hydrovoltaic power generation |
| **2D materials research** | Functionalized graphene oxide (GO) with -OH / -COOH / -NH₂ groups and tunable oxidation degree |
| **Research & teaching** | From zero to a working LAMMPS setup in minutes — ideal for students and researchers new to MD |

## Features (implemented)

- **3D channel builder** — slit graphene / GO nanochannels with tunable oxidation degree and functional groups (-OH / -COOH / -NH₂)
- **Water & ions** — TIP3P (default) and SPC/E water; NaCl / KCl / CaCl₂ with concentration control
- **One-click LAMMPS generation** — `system.data` + `in.streaming.lammps` with the gravity / streaming NEMD template built in (y/z-only thermostat, `fix addforce`, SHAKE, PPPM, rigid membranes)
- **Physics checks** — charge neutrality, channel-height, and ion-statistics warnings
- **WSL-ready scripts** — generated inputs run as-is on WSL or any Linux cluster, GPU flags included (`lmp -sf gpu -pk gpu 1`)
- **Bilingual UI (中文 / English)** with dark & light themes
- **Fully offline & open source** — MIT license, no cloud, no registration

## Roadmap

- One-click analysis: velocity profile → slip length λ, ion flux → streaming current I
- Batch scan matrix (systematic parameter sweeps)
- Environment wizard (one-click WSL / LAMMPS setup)
- OVITO trajectory preview integration
- Windows one-click installer

## Architecture

```
NanoMD Designer (Windows GUI, PySide6 + pyvista)
   │  3D channel builder → force fields → physics checks
   ▼
generate system.data + in.streaming.lammps
   │
   ▼
run anywhere:
  WSL / Linux cluster:  lmp -sf gpu -pk gpu 1 -in in.streaming.lammps
```

## Requirements

- Windows 10/11 with Python 3.10+
- A LAMMPS binary (e.g. inside WSL or on a cluster) for running the generated scripts
- Optional: NVIDIA GPU + CUDA for GPU-accelerated runs

## Installation

```bash
git clone https://github.com/HUC-he/nanomd-designer.git
cd nanomd-designer
python -m venv .venv
.venv\Scripts\pip install -e ".[gui]"
```

Launch:

```bash
.venv\Scripts\pythonw -m nanomd.gui.main
```

or double-click `scripts/launch_gui.bat`.

## Quick start

1. Launch the GUI (double-click `scripts/launch_gui.bat` or use the desktop shortcut).
2. Adjust box size, wall positions, water model, salt and concentration.
3. Set oxidation degree and functional groups to build GO channels.
4. Click **Build & preview** to see the 3D system.
5. Click **Generate LAMMPS scripts** to export `system.data` + `in.streaming.lammps`.
6. Run in WSL: `lmp -sf gpu -pk gpu 1 -in in.streaming.lammps`

## Examples

- `examples/graphene-slit-nacl/` — pristine graphene slit, TIP3P water, 0.6 M NaCl (8550 atoms)
- `examples/go-oh-10-slit/` — GO-10% hydroxylated channel (9410 atoms)

## Documentation

- [User manual (zh)](docs/zh/README.md) / [User manual (en)](docs/en/README.md)
- [UI theme spec](docs/design/theme.md)
- [Design & roadmap](DESIGN.md)

## License & citation

[MIT](LICENSE) · [CITATION.cff](CITATION.cff)

## Contact

shiyuhe1@163.com
