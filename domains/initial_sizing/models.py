"""Typed models for low-fidelity initial sizing inputs and outputs.

The first extraction from MaCa uses mixed aerospace units. Field names carry
the unit convention explicitly so later equation ports do not hide units:
weights are pounds, wing loading is lb/ft^2, distances are nautical miles,
altitudes are feet, and TSFC values are 1/s.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Literal


SegmentName = Literal["takeoff", "climb", "cruise", "loiter", "dash", "landing"]


def _require_finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite.")


def _require_positive(name: str, value: float) -> None:
    _require_finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive.")


def _require_non_negative(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative.")


def _require_fraction(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be between 0 and 1.")


@dataclass(frozen=True)
class InitialSizingAircraftInputs:
    """Aircraft-level inputs for MaCa-style initial sizing.

    These fields mirror the useful MaCa `AircraftData` surface without copying
    the calculation code.
    """

    fixed_weight_lb: float
    initial_takeoff_weight_guess_lb: float
    wing_loading_lb_per_ft2: float
    thrust_to_weight_ratio: float
    cruise_drag_coefficient: float
    cruise_tsfc_per_s: float
    loiter_drag_coefficient: float
    loiter_tsfc_per_s: float
    dash_drag_coefficient: float
    dash_tsfc_per_s: float
    oswald_efficiency: float
    wing_aspect_ratio: float

    def __post_init__(self) -> None:
        _require_non_negative("fixed_weight_lb", self.fixed_weight_lb)
        _require_positive(
            "initial_takeoff_weight_guess_lb", self.initial_takeoff_weight_guess_lb
        )
        _require_positive("wing_loading_lb_per_ft2", self.wing_loading_lb_per_ft2)
        _require_positive("thrust_to_weight_ratio", self.thrust_to_weight_ratio)
        _require_positive("cruise_drag_coefficient", self.cruise_drag_coefficient)
        _require_positive("cruise_tsfc_per_s", self.cruise_tsfc_per_s)
        _require_positive("loiter_drag_coefficient", self.loiter_drag_coefficient)
        _require_positive("loiter_tsfc_per_s", self.loiter_tsfc_per_s)
        _require_positive("dash_drag_coefficient", self.dash_drag_coefficient)
        _require_positive("dash_tsfc_per_s", self.dash_tsfc_per_s)
        _require_positive("oswald_efficiency", self.oswald_efficiency)
        if self.oswald_efficiency > 1.5:
            raise ValueError("oswald_efficiency is outside the low-fidelity model range.")
        _require_positive("wing_aspect_ratio", self.wing_aspect_ratio)


@dataclass(frozen=True)
class MissionSegmentInput:
    """One ordered mission segment for initial sizing.

    Required fields depend on `name`:
    cruise and dash require distance, altitude, and Mach; loiter requires
    endurance, altitude, and Mach; takeoff, climb, and landing do not require
    additional fields for the first MaCa extraction.
    """

    name: SegmentName
    distance_nm: float | None = None
    altitude_ft: float | None = None
    mach: float | None = None
    endurance_min: float | None = None

    def __post_init__(self) -> None:
        if self.name not in {"takeoff", "climb", "cruise", "loiter", "dash", "landing"}:
            raise ValueError(f"Unsupported mission segment name: {self.name!r}.")

        if self.distance_nm is not None:
            _require_positive("distance_nm", self.distance_nm)
        if self.altitude_ft is not None:
            _require_non_negative("altitude_ft", self.altitude_ft)
        if self.mach is not None:
            _require_positive("mach", self.mach)
        if self.endurance_min is not None:
            _require_positive("endurance_min", self.endurance_min)

        if self.name in {"cruise", "dash"}:
            self._require_present("distance_nm", self.distance_nm)
            self._require_present("altitude_ft", self.altitude_ft)
            self._require_present("mach", self.mach)
        if self.name == "loiter":
            self._require_present("altitude_ft", self.altitude_ft)
            self._require_present("mach", self.mach)
            self._require_present("endurance_min", self.endurance_min)

    @staticmethod
    def _require_present(name: str, value: float | None) -> None:
        if value is None:
            raise ValueError(f"{name} is required for this mission segment.")


@dataclass(frozen=True)
class InitialSizingInputs:
    """Complete input object for a standalone initial sizing run."""

    aircraft: InitialSizingAircraftInputs
    mission_segments: tuple[MissionSegmentInput, ...]
    convergence_tolerance_lb: float = 10.0
    max_iterations: int = 250

    def __post_init__(self) -> None:
        if not self.mission_segments:
            raise ValueError("mission_segments must contain at least one segment.")
        _require_positive("convergence_tolerance_lb", self.convergence_tolerance_lb)
        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be positive.")


@dataclass(frozen=True)
class SegmentSizingResult:
    """Traceable output for one mission segment in a sizing run."""

    segment_label: str
    fuel_burn_lb: float
    beta_weight_fraction: float

    def __post_init__(self) -> None:
        if not self.segment_label:
            raise ValueError("segment_label must not be empty.")
        _require_non_negative("fuel_burn_lb", self.fuel_burn_lb)
        _require_fraction("beta_weight_fraction", self.beta_weight_fraction)


@dataclass(frozen=True)
class InitialSizingOutputs:
    """Typed outputs for the future MaCa initial sizing extraction."""

    converged_takeoff_weight_lb: float
    fuel_weight_lb: float
    empty_weight_lb: float
    fuel_fraction: float
    structure_fraction: float
    segment_results: tuple[SegmentSizingResult, ...] = field(default_factory=tuple)
    iterations: int = 0
    converged: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)
    assumptions: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_positive("converged_takeoff_weight_lb", self.converged_takeoff_weight_lb)
        _require_non_negative("fuel_weight_lb", self.fuel_weight_lb)
        _require_non_negative("empty_weight_lb", self.empty_weight_lb)
        _require_fraction("fuel_fraction", self.fuel_fraction)
        _require_fraction("structure_fraction", self.structure_fraction)
        if self.fuel_fraction + self.structure_fraction > 1.0:
            raise ValueError("fuel_fraction plus structure_fraction must not exceed 1.")
        if self.iterations < 0:
            raise ValueError("iterations must be non-negative.")
