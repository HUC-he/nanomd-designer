# Contributing to NanoMD Designer

Thanks for your interest! This project is open to contributions of any size —
bug reports, documentation, translations, and code.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development environment

The project targets **Windows + WSL** as the primary platform.

### 1. Clone & install

```bash
git clone https://github.com/shiyuhe1/nanomd-designer.git
cd nanomd-designer
python -m pip install -e ".[gui,analysis,dev]"
```

Requires Python 3.10+.

### 2. Run the app / CLI

```bash
nanomd-gui   # GUI
nanomd       # headless CLI
```

### 3. Lint & test

```bash
ruff check .
pytest
```

GUI tests are skipped automatically when no display is available.

## Project layout

- `src/nanomd/core/` — engine, **no GUI dependencies** (must stay headless-testable)
- `src/nanomd/gui/` — PySide6 UI
- `scripts/wsl/` — bash helpers run inside WSL (environment check / setup / run)
- `docs/` — zh & en documentation, design specs
- `tests/` — pytest suite

## WSL-side development

The WSL bridge uses only `wsl.exe` subprocesses and file exchange. When changing
`scripts/wsl/*.sh`, validate syntax with:

```bash
wsl -e bash -n scripts/wsl/env_check.sh
wsl -e bash -n scripts/wsl/run_job.sh
wsl -e bash -n scripts/wsl/setup_wsl_env.sh
```

## Pull request process

1. Fork the repo and create a branch (`feature/...`, `fix/...`).
2. Keep changes small and focused; add tests for `core/` changes.
3. Run `ruff check .` and `pytest` locally.
4. Open a PR with a clear description; reference any related issue.

## Commit style

Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.

## Contact

Maintainer: shiyuhe1@163.com
