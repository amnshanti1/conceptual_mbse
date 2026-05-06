"""Typed models for low-fidelity constraint analysis.

These models prepare for extracting MaCa `ConstraintAnalysis.py` without
bringing over plotting, CSV output, or loose scenario dictionaries. Field names
use MaCa-compatible aerospace units: wing loading is lb/ft^2, thrust is pounds,
density is slug/ft^3, speed is ft/s, runway distances are feet, and load factors
and thrust loading are dimensionless.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite


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


def _require_optional_positive(name: str, value: float | None) -> None:
    if value is not None:
        _require_positive(name, value)


def _require_optional_non_negative(name: str, value: float | None) -> None:
    if value is not None:
        _require_non_negative(name, value)


@dataclass(frozen=True)
class ConstraintScenarioInput:
    """One named constraint scenario from MaCa's default parameter set.

    Optional fields support the different MaCa curve families: generic
    cruise-like constraints, turn constraints, excess-power constraints,
    takeoff, and landing.
    """

    name: str
    beta_weight_fraction: float
    zero_lift_drag_coefficient: float
    density_slug_per_ft3: float
    alpha_dry: float | None = None
    alpha_afterburner: float | None = None
    use_afterburner: bool = False
    induced_drag_k1: float | None = None
    induced_drag_k2: float | None = None
    speed_of_sound_ft_per_s: float | None = None
    mach: float | None = None
    load_factor: float | None = None
    excess_specific_power_ft_per_s: float | None = None
    velocity_ft_per_s: float | None = None
    maximum_lift_coefficient: float | None = None
    takeoff_speed_factor: float | None = None
    landing_speed_factor: float | None = None
    runway_distance_ft: float | None = None
    rolling_friction_coefficient: float | None = None
    gravity_ft_per_s2: float | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty.")
        _require_positive("beta_weight_fraction", self.beta_weight_fraction)
        if self.beta_weight_fraction > 1.5:
            raise ValueError("beta_weight_fraction is outside the low-fidelity model range.")
        _require_positive("zero_lift_drag_coefficient", self.zero_lift_drag_coefficient)
        _require_positive("density_slug_per_ft3", self.density_slug_per_ft3)
        _require_optional_positive("alpha_dry", self.alpha_dry)
        _require_optional_positive("alpha_afterburner", self.alpha_afterburner)
        _require_optional_positive("speed_of_sound_ft_per_s", self.speed_of_sound_ft_per_s)
        _require_optional_positive("mach", self.mach)
        _require_optional_positive("load_factor", self.load_factor)
        _require_optional_non_negative(
            "excess_specific_power_ft_per_s", self.excess_specific_power_ft_per_s
        )
        _require_optional_positive("velocity_ft_per_s", self.velocity_ft_per_s)
        _require_optional_positive(
            "maximum_lift_coefficient", self.maximum_lift_coefficient
        )
        _require_optional_positive("takeoff_speed_factor", self.takeoff_speed_factor)
        _require_optional_positive("landing_speed_factor", self.landing_speed_factor)
        _require_optional_positive("runway_distance_ft", self.runway_distance_ft)
        _require_optional_non_negative(
            "rolling_friction_coefficient", self.rolling_friction_coefficient
        )
        _require_optional_positive("gravity_ft_per_s2", self.gravity_ft_per_s2)

        if self.use_afterburner and self.alpha_afterburner is None:
            raise ValueError("alpha_afterburner is required when use_afterburner is true.")


@dataclass(frozen=True)
class ConstraintAnalysisInputs:
    """Complete input object for a standalone constraint analysis run."""

    wing_loading_values_lb_per_ft2: tuple[float, ...]
    maximum_thrust_lb: float
    military_thrust_lb: float
    scenarios: tuple[ConstraintScenarioInput, ...]

    def __post_init__(self) -> None:
        if not self.wing_loading_values_lb_per_ft2:
            raise ValueError("wing_loading_values_lb_per_ft2 must not be empty.")
        for value in self.wing_loading_values_lb_per_ft2:
            _require_positive("wing_loading_values_lb_per_ft2 item", value)
        _require_positive("maximum_thrust_lb", self.maximum_thrust_lb)
        _require_positive("military_thrust_lb", self.military_thrust_lb)
        if self.military_thrust_lb > self.maximum_thrust_lb:
            raise ValueError("military_thrust_lb must not exceed maximum_thrust_lb.")
        if not self.scenarios:
            raise ValueError("scenarios must contain at least one constraint scenario.")


@dataclass(frozen=True)
class ConstraintCurveResult:
    """Plot-ready, equation-free result for one constraint curve."""

    name: str
    required_thrust_to_weight: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty.")
        if not self.required_thrust_to_weight:
            raise ValueError("required_thrust_to_weight must not be empty.")
        for value in self.required_thrust_to_weight:
            _require_non_negative("required_thrust_to_weight item", value)


@dataclass(frozen=True)
class ConstraintAnalysisOutputs:
    """Typed outputs for the future MaCa constraint analysis extraction."""

    wing_loading_values_lb_per_ft2: tuple[float, ...]
    curves: tuple[ConstraintCurveResult, ...]
    envelope_thrust_to_weight: tuple[float, ...]
    selected_wing_loading_lb_per_ft2: float | None = None
    selected_thrust_to_weight: float | None = None
    landing_wing_loading_limit_lb_per_ft2: float | None = None
    feasible_mask: tuple[bool, ...] | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
    assumptions: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.wing_loading_values_lb_per_ft2:
            raise ValueError("wing_loading_values_lb_per_ft2 must not be empty.")
        for value in self.wing_loading_values_lb_per_ft2:
            _require_positive("wing_loading_values_lb_per_ft2 item", value)
        if not self.curves:
            raise ValueError("curves must contain at least one curve.")
        if len(self.envelope_thrust_to_weight) != len(self.wing_loading_values_lb_per_ft2):
            raise ValueError(
                "envelope_thrust_to_weight must match wing_loading_values_lb_per_ft2 length."
            )
        for value in self.envelope_thrust_to_weight:
            _require_non_negative("envelope_thrust_to_weight item", value)
        for curve in self.curves:
            if len(curve.required_thrust_to_weight) != len(
                self.wing_loading_values_lb_per_ft2
            ):
                raise ValueError("Each curve must match the wing loading vector length.")
        _require_optional_positive(
            "selected_wing_loading_lb_per_ft2", self.selected_wing_loading_lb_per_ft2
        )
        _require_optional_non_negative(
            "selected_thrust_to_weight", self.selected_thrust_to_weight
        )
        _require_optional_positive(
            "landing_wing_loading_limit_lb_per_ft2",
            self.landing_wing_loading_limit_lb_per_ft2,
        )
        if self.feasible_mask is not None and len(self.feasible_mask) != len(
            self.wing_loading_values_lb_per_ft2
        ):
            raise ValueError("feasible_mask must match the wing loading vector length.")
