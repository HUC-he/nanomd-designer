"""Command-line interface for NanoMD Designer (headless mode)."""

from __future__ import annotations

import argparse

from nanomd import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nanomd",
        description="NanoMD Designer - nanochannel MD design & WSL runner (headless).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.parse_args(argv)
    print("NanoMD Designer is ready (M0). Full CLI tools arrive with M1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
