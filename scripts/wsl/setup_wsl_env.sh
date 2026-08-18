#!/usr/bin/env bash
# NanoMD Designer - WSL environment setup (standard mode)
#
# Installs Miniconda + LAMMPS (CPU, conda-forge) + packmol inside WSL.
# The GUI environment wizard runs this script automatically.
#
# Usage:
#   bash setup_wsl_env.sh                 # official sources
#   MIRROR=1 bash setup_wsl_env.sh        # TUNA mirror (faster in CN)
set -euo pipefail

ENV_NAME="${ENV_NAME:-nanomd}"
CONDA_DIR="$HOME/miniconda3"

echo "==> [1/3] Check / install Miniconda ($CONDA_DIR)"
if [ ! -x "$CONDA_DIR/bin/conda" ]; then
  if [ "${MIRROR:-0}" = "1" ]; then
    URL="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh"
  else
    URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
  fi
  echo "    Downloading Miniconda ..."
  curl -fsSL "$URL" -o /tmp/miniconda.sh
  bash /tmp/miniconda.sh -b -p "$CONDA_DIR"
  rm -f /tmp/miniconda.sh
else
  echo "    Found existing Miniconda."
fi

echo "==> [2/3] Create environment '$ENV_NAME' (lammps + packmol)"
if ! "$CONDA_DIR/bin/conda" env list | grep -qE "^\s*${ENV_NAME}\s"; then
  "$CONDA_DIR/bin/conda" create -n "$ENV_NAME" -y -c conda-forge lammps packmol
else
  echo "    Environment '$ENV_NAME' exists; installing packages if missing."
  "$CONDA_DIR/bin/conda" install -n "$ENV_NAME" -y -c conda-forge lammps packmol
fi

echo "==> [3/3] Verify"
LMP="$CONDA_DIR/envs/$ENV_NAME/bin/lmp"
if [ -x "$LMP" ]; then
  echo "    LAMMPS: $LMP"
  "$LMP" -h | head -n 3 || true
  echo "    Done. Run the NanoMD environment wizard again to confirm."
else
  echo "    ERROR: $LMP not found. Check the install log above." >&2
  exit 1
fi
