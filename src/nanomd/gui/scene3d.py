"""3D rendering of generated structures (pyvista)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv

from nanomd.core.models.structure import Structure
from nanomd.gui.theme import ATOM_COLORS, hex_to_rgb


def _rgb_array(structure: Structure) -> np.ndarray:
    return np.asarray(
        [
            hex_to_rgb(ATOM_COLORS.get(atom.type_name, "#AAAAAA"))
            for atom in structure.atoms
        ],
        dtype=np.uint8,
    )


def add_structure(plotter: pv.Plotter, structure: Structure, point_size: float = 4.0) -> None:
    """Draw all atoms as colored spheres (walls gray, water red/white, ions
    colored by species)."""
    if structure.n_atoms == 0:
        return
    plotter.add_points(
        structure.positions_array(),
        scalars=_rgb_array(structure),
        rgb=True,
        point_size=point_size,
        render_points_as_spheres=True,
    )


def render_offscreen(
    structure: Structure,
    path: str | Path,
    point_size: float = 4.0,
    view: str = "isometric",
    window_size: tuple[int, int] = (1600, 1000),
) -> Path:
    """Render the structure to a PNG without opening a window."""
    path = Path(path)
    plotter = pv.Plotter(off_screen=True, window_size=window_size)
    add_structure(plotter, structure, point_size=point_size)
    plotter.show_axes()
    if view == "top":
        plotter.view_xy()
    else:
        plotter.camera_position = "iso"
    plotter.screenshot(path)
    plotter.close()
    return path
