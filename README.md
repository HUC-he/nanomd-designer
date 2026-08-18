# NanoMD Designer

[![CI](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml/badge.svg)](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**Design nanochannel MD systems on Windows, run them in WSL, and get results back — without touching the terminal.**

NanoMD Designer is an open-source, bilingual (中文 / EN) desktop GUI for molecular dynamics (MD) simulations of nanofluidics and electrochemical interfaces with [LAMMPS](https://www.lammps.org). It targets materials & chemistry researchers who work on Windows and do not want to hand-write LAMMPS input scripts or learn Linux.

## Features

- **3D channel builder** — slit graphene / GO nanochannels with tunable oxidation degree and functional groups (-OH / -COOH / -NH₂)
- **Water & ions** — TIP3P (default) and SPC/E water; NaCl / KCl / CaCl₂ with concentration control
- **One-click input generation** — LAMMPS `data` + `in` files with the streaming / gravity NEMD workflow built in (y/z-only thermostat, `fix addforce`, SHAKE, PPPM)
- **Physics validator** — beginner-friendly warnings for channel height, ion statistics, charge neutrality, flow-speed target, and more
- **WSL bridge** — auto-detect WSL / LAMMPS / GPU, sync job files, run, stream logs back live, and copy results to a Windows output folder
- **One-click analysis** — velocity profile → slip length λ, ion flux → streaming current I, density profile → surface charge σ, Poisson integration → streaming potential V
- **Batch scan** — parameter sweep matrix (5 ns screening → 20 ns production) with resume and sensitivity ranking plots
- **Bilingual UI (中文 / English)** with dark & light themes

## Architecture

```
Windows GUI (PySide6)  -- generate -->  project files
     |  sync via wsl.exe                       |
     +-----------------------------------------+
WSL backend: run_job.sh -> lmp (GPU optional)
     |  stdout streamed back via tee
Windows GUI: live progress / thermo plots / analysis / OVITO
```

The GUI never requires the user to open a shell. An "export scripts only" mode is kept for advanced users and remote clusters.

## Requirements

- Windows 10/11 with WSL2 and a Linux distro (Ubuntu 24.04 recommended)
- LAMMPS inside WSL — the built-in **environment wizard** can install a conda CPU build automatically (GPU build guided if CUDA is detected)
- Optional: NVIDIA GPU with CUDA for GPU acceleration; packmol for improved water packing; OVITO for trajectory viewing

## Installation (development)

```bash
pip install -e ".[gui,analysis,dev]"
```

Run it:

```bash
nanomd       # headless CLI
nanomd-gui   # GUI
```

End users will get a one-click Windows installer in a later release.

## Quick start

1. Start `nanomd-gui` — the environment wizard checks WSL / LAMMPS / GPU.
2. Create a project, pick a template (e.g. graphene slit 1 nm + TIP3P + 0.6 M NaCl).
3. Tune the geometry in 3D, then click **Generate & Run**.
4. Watch live thermo curves, then analyze and export publication figures.

## Documentation

- [User manual (zh)](docs/zh/README.md) / [User manual (en)](docs/en/README.md)
- [UI theme spec](docs/design/theme.md)
- [Design & roadmap](DESIGN.md)

## License

[MIT](LICENSE)

## Contact

shiyuhe1@163.com

## Citation

If you use this software in your research, please cite it (see [CITATION.cff](CITATION.cff)).
