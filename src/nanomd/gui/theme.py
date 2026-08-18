"""Theme loading (dark "Deep Channel" / light "Clear Water")."""

from __future__ import annotations

from pathlib import Path

THEME_NAMES = ("dark", "light")

_CANDIDATES = (
    Path(__file__).resolve().parents[3] / "assets" / "themes",  # repo layout
    Path(__file__).resolve().parents[1] / "assets" / "themes",  # packaged layout
)

ATOM_COLORS: dict[str, str] = {
    "C": "#8A97A6",
    "C_OH": "#8A97A6",
    "C_NH2": "#8A97A6",
    "O_w": "#E5484D",
    "H_w": "#F2F4F8",
    "O_g": "#E5484D",
    "H_g": "#F2F4F8",
    "Na+": "#9D7BFF",
    "Cl-": "#35C4C0",
    "K+": "#E58C4A",
    "Ca2+": "#2E8FB8",
    "N_amine": "#60A5FA",
    "H_amine": "#F2F4F8",
    "C_carboxyl": "#8A97A6",
    "O_c(=O)": "#E5484D",
    "O_c(-OH)": "#E5484D",
    "H_c": "#F2F4F8",
}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def load_qss(name: str) -> str:
    if name not in THEME_NAMES:
        raise ValueError(f"unknown theme: {name!r}")
    for root in _CANDIDATES:
        candidate = root / f"{name}.qss"
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(f"theme file for {name!r} not found")


def apply_theme(app, name: str) -> None:
    app.setStyleSheet(load_qss(name))
