#!/usr/bin/env bash
# NanoMD Designer - WSL environment check
#
# Prints key: value lines that the Windows GUI parses to build the
# environment health report. Safe to run repeatedly.
set -u

report() { echo "$1"; }

if [ -r /etc/os-release ]; then
  report "distro: $(grep -E '^(NAME|VERSION_ID)=' /etc/os-release | tr '\n' ' ')"
else
  report "distro: unknown"
fi

LMP=""
for c in \
  "$HOME/lammps/bin/lmp" \
  "$HOME/miniconda3/envs/nanomd/bin/lmp" \
  "$HOME/miniconda3/bin/lmp"; do
  if [ -x "$c" ]; then LMP="$c"; break; fi
done
if [ -z "$LMP" ] && command -v lmp >/dev/null 2>&1; then
  LMP="$(command -v lmp)"
fi
report "lmp_path: ${LMP:-}"

if [ -n "$LMP" ]; then
  if "$LMP" -h 2>/dev/null | grep -qi gpu; then
    report "lmp_gpu: yes"
  else
    report "lmp_gpu: no"
  fi
fi

if [ -e /usr/lib/wsl/lib/libcuda.so.1 ] || command -v nvidia-smi >/dev/null 2>&1; then
  report "gpu: yes"
  if command -v nvidia-smi >/dev/null 2>&1; then
    report "gpu_name: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n 1)"
  fi
else
  report "gpu: no"
fi

PACKMOL=""
for c in \
  "$HOME/miniconda3/envs/nanomd/bin/packmol" \
  "$HOME/miniconda3/bin/packmol"; do
  if [ -x "$c" ]; then PACKMOL="$c"; break; fi
done
if [ -z "$PACKMOL" ] && command -v packmol >/dev/null 2>&1; then
  PACKMOL="$(command -v packmol)"
fi
report "packmol: ${PACKMOL:-}"
