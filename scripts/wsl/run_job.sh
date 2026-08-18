#!/usr/bin/env bash
# NanoMD Designer - job runner (called by the Windows GUI via wsl.exe)
#
# Usage:
#   LMP_BIN=/path/to/lmp bash run_job.sh <console_log_path> [lmp args...]
#
# - Runs from the job directory (the GUI sets cwd to ~/nanomd-jobs/<job>).
# - Streams LAMMPS stdout to a Windows-visible log via tee, so the GUI can
#   tail it live.
set -uo pipefail

CONSOLE="${1:?usage: run_job.sh <console_log_path> [lmp args...]}"
shift
LMP_BIN="${LMP_BIN:-lmp}"

mkdir -p "$(dirname "$CONSOLE")"
echo "==> LAMMPS: $LMP_BIN $*"
echo "==> Console log: $CONSOLE"

"$LMP_BIN" "$@" 2>&1 | tee "$CONSOLE"
status="${PIPESTATUS[0]}"

echo "==> LAMMPS exit code: $status"
exit "$status"
