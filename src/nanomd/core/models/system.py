"""Core data structures for simulation systems (M1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from nanomd.core.forcefields.library import FUNCTIONAL_GROUPS


@dataclass(frozen=True)
class Box:
    """Orthorhombic simulation box, lengths in Angstrom."""

    lx: float
    ly: float
    lz: float

    def __post_init__(self) -> None:
        if min(self.lx, self.ly, self.lz) <= 0:
            raise ValueError("box lengths must be positive")


@dataclass(frozen=True)
class SlitChannel:
    """Two parallel walls along z (flow direction is x, periodic x/y).

    ``lower_wall_z`` / ``upper_wall_z`` are the *inner surfaces* of the two
    membranes. The channel height is their distance.
    """

    box: Box
    lower_wall_z: float
    upper_wall_z: float

    def __post_init__(self) -> None:
        if not (0.0 < self.lower_wall_z < self.upper_wall_z < self.box.lz):
            raise ValueError("wall positions must satisfy 0 < lower < upper < Lz")

    @property
    def height(self) -> float:
        """Channel height (distance between inner wall surfaces), Angstrom."""
        return self.upper_wall_z - self.lower_wall_z

    @property
    def channel_volume(self) -> float:
        """Volume of the fluid region between the walls, Angstrom^3."""
        return self.box.lx * self.box.ly * self.height


@dataclass
class WaterSpec:
    """Water filling specification."""

    model_key: str = "tip3p"
    density_g_cm3: float = 1.0
    n_molecules: int | None = None


@dataclass
class IonSpec:
    """Salt specification for the channel fluid."""

    salt: str = "NaCl"
    concentration_molar: float = 0.6
    ion_set: str = "spec"


@dataclass
class MembraneSpec:
    """Membrane material and functionalization."""

    material: str = "graphene"  # "graphene" | "go"
    oxidation_fraction: float = 0.0  # 0..1, fraction of surface carbons modified
    functional_groups: tuple[str, ...] = ("oh",)

    def __post_init__(self) -> None:
        if not 0.0 <= self.oxidation_fraction <= 1.0:
            raise ValueError("oxidation_fraction must be in [0, 1]")
        for key in self.functional_groups:
            if key not in FUNCTIONAL_GROUPS:
                raise ValueError(f"unknown functional group: {key!r}")


@dataclass
class System:
    """A complete simulation system description."""

    name: str
    channel: SlitChannel
    membrane: MembraneSpec = field(default_factory=MembraneSpec)
    water: WaterSpec = field(default_factory=WaterSpec)
    ions: IonSpec | None = field(default_factory=IonSpec)
    temperature_k: float = 300.0
    target_velocity_ang_per_ps: float = 0.5
    drive_force_kcal_mol_ang: float = 0.0005
    seed: int = 12345

    def __post_init__(self) -> None:
        if self.temperature_k <= 0:
            raise ValueError("temperature must be positive")
        if self.target_velocity_ang_per_ps <= 0:
            raise ValueError("target velocity must be positive")
        if self.drive_force_kcal_mol_ang <= 0:
            raise ValueError("drive force must be positive")

    def summary(self) -> str:
        """Human-readable one-line description."""
        salt = self.ions.salt if self.ions else "none"
        conc = self.ions.concentration_molar if self.ions else 0.0
        ox = f"{self.membrane.oxidation_fraction:.0%}" if self.membrane.material == "go" else "-"
        return (
            f"{self.name}: {self.membrane.material}(ox {ox}), "
            f"h={self.channel.height:.1f} A, {self.water.model_key} water, "
            f"{salt} {conc:.2f} M, T={self.temperature_k:.0f} K"
        )
