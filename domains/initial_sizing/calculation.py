"""Low-fidelity initial sizing calculation extracted from MaCa.

This module ports the smallest working MaCa calculation path:

- mission segment weight fractions from `Segments.py`
- takeoff weight convergence from `MissionAnalysisNew.converge_weight`

It intentionally excludes MaCa's CSV loading, plotting, prompts, and sweep
helpers. Inputs and outputs are typed by `domains.initial_sizing.models`.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite

from domains.initial_sizing.models import (
    InitialSizingAircraftInputs,
    InitialSizingInputs,
    InitialSizingOutputs,
    MissionSegmentInput,
    SegmentSizingResult,
)


FT_PER_NM = 6076.12
M_PER_FT = 0.3048

MACA_ASSUMPTIONS = (
    "MaCa-compatible mixed aerospace units are used internally.",
    "Takeoff mission weight fraction is fixed at 0.98.",
    "Climb mission weight fraction is 1.0065 - 0.0325 * 0.87.",
    "Landing segment fuel burn is zero.",
    "Cruise, loiter, and dash use MaCa Breguet-style weight fraction equations.",
    "Empty weight uses MaCa's Raymer-style placeholder empirical fraction.",
    "Weight convergence updates the assumed takeoff weight by half the residual.",
)


@dataclass(frozen=True)
class _AtmosphereState:
    density_slug_per_ft3: float
    speed_of_sound_ft_per_s: float


@dataclass(frozen=True)
class _SegmentState:
    current_weight_lb: float
    beta_weight_fraction: float
    fuel_burned_lb: float


def run_initial_sizing(inputs: InitialSizingInputs) -> InitialSizingOutputs:
    """Run MaCa-style low-fidelity initial sizing.

    The calculation preserves MaCa behavior for a typed in-memory input object.
    It performs no file I/O and creates no plots.
    """

    assumed_takeoff_weight_lb = inputs.aircraft.initial_takeoff_weight_guess_lb
    last_segment_results: tuple[SegmentSizingResult, ...] = ()
    new_takeoff_weight_lb = assumed_takeoff_weight_lb
    fuel_weight_lb = 0.0
    empty_weight_lb = 0.0
    converged = False
    iterations = 0

    for iteration in range(1, inputs.max_iterations + 1):
        iterations = iteration
        state = _SegmentState(
            current_weight_lb=assumed_takeoff_weight_lb,
            beta_weight_fraction=1.0,
            fuel_burned_lb=0.0,
        )
        segment_results: list[SegmentSizingResult] = []
        segment_counts: dict[str, int] = {}

        for segment in inputs.mission_segments:
            fuel_before_lb = state.fuel_burned_lb
            state = _run_segment(inputs.aircraft, segment, state)
            fuel_delta_lb = max(0.0, state.fuel_burned_lb - fuel_before_lb)
            segment_counts[segment.name] = segment_counts.get(segment.name, 0) + 1
            segment_results.append(
                SegmentSizingResult(
                    segment_label=f"{segment.name} {segment_counts[segment.name]}",
                    fuel_burn_lb=fuel_delta_lb,
                    beta_weight_fraction=float(state.beta_weight_fraction),
                )
            )

        empty_weight_fraction = _empty_weight_fraction(
            aircraft=inputs.aircraft,
            assumed_takeoff_weight_lb=assumed_takeoff_weight_lb,
        )
        fuel_weight_lb = state.fuel_burned_lb
        empty_weight_lb = empty_weight_fraction * assumed_takeoff_weight_lb
        new_takeoff_weight_lb = (
            inputs.aircraft.fixed_weight_lb + empty_weight_lb + fuel_weight_lb
        )
        residual_lb = new_takeoff_weight_lb - assumed_takeoff_weight_lb
        last_segment_results = tuple(segment_results)

        if abs(residual_lb) < inputs.convergence_tolerance_lb:
            converged = True
            break

        assumed_takeoff_weight_lb += residual_lb / 2.0

    fuel_fraction = fuel_weight_lb / new_takeoff_weight_lb
    structure_fraction = empty_weight_lb / new_takeoff_weight_lb
    warnings = ()
    if not converged:
        warnings = (
            f"Initial sizing did not converge in {inputs.max_iterations} iterations.",
        )

    return InitialSizingOutputs(
        converged_takeoff_weight_lb=float(new_takeoff_weight_lb),
        fuel_weight_lb=float(fuel_weight_lb),
        empty_weight_lb=float(empty_weight_lb),
        fuel_fraction=float(fuel_fraction),
        structure_fraction=float(structure_fraction),
        segment_results=last_segment_results,
        iterations=iterations,
        converged=converged,
        warnings=warnings,
        assumptions=MACA_ASSUMPTIONS,
    )


def _run_segment(
    aircraft: InitialSizingAircraftInputs,
    segment: MissionSegmentInput,
    state: _SegmentState,
) -> _SegmentState:
    if segment.name == "takeoff":
        return _takeoff_segment(state)
    if segment.name == "climb":
        return _climb_segment(state)
    if segment.name == "cruise":
        return _cruise_segment(aircraft, segment, state)
    if segment.name == "loiter":
        return _loiter_segment(aircraft, segment, state)
    if segment.name == "dash":
        return _dash_segment(aircraft, segment, state)
    if segment.name == "landing":
        return state
    raise ValueError(f"Unsupported mission segment name: {segment.name!r}.")


def _takeoff_segment(state: _SegmentState) -> _SegmentState:
    weight_fraction = 0.98
    fuel_burn_lb = (1.0 - weight_fraction) * state.current_weight_lb
    return _apply_segment_weight_fraction(state, weight_fraction, fuel_burn_lb)


def _climb_segment(state: _SegmentState) -> _SegmentState:
    mach_climb = 0.87
    weight_fraction = 1.0065 - 0.0325 * mach_climb
    fuel_burn_lb = (1.0 - weight_fraction) * state.current_weight_lb
    return _apply_segment_weight_fraction(state, weight_fraction, fuel_burn_lb)


def _cruise_segment(
    aircraft: InitialSizingAircraftInputs,
    segment: MissionSegmentInput,
    state: _SegmentState,
) -> _SegmentState:
    distance_ft = _required(segment.distance_nm, "distance_nm") * FT_PER_NM
    atmosphere = _standard_atmosphere(_required(segment.altitude_ft, "altitude_ft") * M_PER_FT)
    velocity_ft_per_s = _required(segment.mach, "mach") * atmosphere.speed_of_sound_ft_per_s
    dynamic_pressure_lb_per_ft2 = (
        0.5 * atmosphere.density_slug_per_ft3 * velocity_ft_per_s**2
    )
    lift_to_drag = _lift_to_drag(
        dynamic_pressure_lb_per_ft2=dynamic_pressure_lb_per_ft2,
        drag_coefficient=aircraft.cruise_drag_coefficient,
        wing_loading_lb_per_ft2=aircraft.wing_loading_lb_per_ft2,
        beta_weight_fraction=state.beta_weight_fraction,
        oswald_efficiency=aircraft.oswald_efficiency,
        wing_aspect_ratio=aircraft.wing_aspect_ratio,
    )
    weight_fraction = exp(
        (-distance_ft * aircraft.cruise_tsfc_per_s)
        / (velocity_ft_per_s * lift_to_drag)
    )
    fuel_burn_lb = (1.0 - weight_fraction) * state.current_weight_lb
    return _apply_segment_weight_fraction(state, weight_fraction, fuel_burn_lb)


def _loiter_segment(
    aircraft: InitialSizingAircraftInputs,
    segment: MissionSegmentInput,
    state: _SegmentState,
) -> _SegmentState:
    endurance_s = _required(segment.endurance_min, "endurance_min") * 60.0
    atmosphere = _standard_atmosphere(_required(segment.altitude_ft, "altitude_ft") * M_PER_FT)
    velocity_ft_per_s = _required(segment.mach, "mach") * atmosphere.speed_of_sound_ft_per_s
    dynamic_pressure_lb_per_ft2 = (
        0.5 * atmosphere.density_slug_per_ft3 * velocity_ft_per_s**2
    )
    lift_to_drag = _lift_to_drag(
        dynamic_pressure_lb_per_ft2=dynamic_pressure_lb_per_ft2,
        drag_coefficient=aircraft.loiter_drag_coefficient,
        wing_loading_lb_per_ft2=aircraft.wing_loading_lb_per_ft2,
        beta_weight_fraction=state.beta_weight_fraction,
        oswald_efficiency=aircraft.oswald_efficiency,
        wing_aspect_ratio=aircraft.wing_aspect_ratio,
    )
    weight_fraction = exp((-endurance_s * aircraft.loiter_tsfc_per_s) / lift_to_drag)
    fuel_burn_lb = (1.0 - weight_fraction) * state.current_weight_lb
    return _apply_segment_weight_fraction(state, weight_fraction, fuel_burn_lb)


def _dash_segment(
    aircraft: InitialSizingAircraftInputs,
    segment: MissionSegmentInput,
    state: _SegmentState,
) -> _SegmentState:
    distance_ft = _required(segment.distance_nm, "distance_nm") * FT_PER_NM
    atmosphere = _standard_atmosphere(_required(segment.altitude_ft, "altitude_ft") * M_PER_FT)
    velocity_ft_per_s = _required(segment.mach, "mach") * atmosphere.speed_of_sound_ft_per_s
    dynamic_pressure_lb_per_ft2 = (
        0.5 * atmosphere.density_slug_per_ft3 * velocity_ft_per_s**2
    )
    lift_to_drag = _lift_to_drag(
        dynamic_pressure_lb_per_ft2=dynamic_pressure_lb_per_ft2,
        drag_coefficient=aircraft.dash_drag_coefficient,
        wing_loading_lb_per_ft2=aircraft.wing_loading_lb_per_ft2,
        beta_weight_fraction=state.beta_weight_fraction,
        oswald_efficiency=aircraft.oswald_efficiency,
        wing_aspect_ratio=aircraft.wing_aspect_ratio,
    )
    weight_fraction = exp(
        (-distance_ft * aircraft.dash_tsfc_per_s)
        / (velocity_ft_per_s * lift_to_drag)
    )
    fuel_burn_lb = (1.0 - weight_fraction) * state.current_weight_lb
    return _apply_segment_weight_fraction(state, weight_fraction, fuel_burn_lb)


def _apply_segment_weight_fraction(
    state: _SegmentState, weight_fraction: float, fuel_burn_lb: float
) -> _SegmentState:
    return _SegmentState(
        current_weight_lb=state.current_weight_lb - fuel_burn_lb,
        beta_weight_fraction=state.beta_weight_fraction * weight_fraction,
        fuel_burned_lb=state.fuel_burned_lb + fuel_burn_lb,
    )


def _lift_to_drag(
    dynamic_pressure_lb_per_ft2: float,
    drag_coefficient: float,
    wing_loading_lb_per_ft2: float,
    beta_weight_fraction: float,
    oswald_efficiency: float,
    wing_aspect_ratio: float,
) -> float:
    beta_wing_loading = wing_loading_lb_per_ft2 * beta_weight_fraction
    parasite_term = dynamic_pressure_lb_per_ft2 * drag_coefficient / beta_wing_loading
    induced_term = beta_wing_loading / (
        dynamic_pressure_lb_per_ft2 * 3.14 * oswald_efficiency * wing_aspect_ratio
    )
    return 1.0 / (parasite_term + induced_term)


def _empty_weight_fraction(
    aircraft: InitialSizingAircraftInputs, assumed_takeoff_weight_lb: float
) -> float:
    a = -0.02
    b = 1.82
    c1 = -0.1
    c2 = 0.2
    c3 = 0.04
    c4 = -0.1
    c5 = 0.08
    return (
        a
        + b
        * assumed_takeoff_weight_lb**c1
        * aircraft.wing_aspect_ratio**c2
        * aircraft.thrust_to_weight_ratio**c3
        * (aircraft.wing_loading_lb_per_ft2**c4 * 2.2**c5)
    )


def _standard_atmosphere(altitude_m: float) -> _AtmosphereState:
    """Return MaCa-compatible atmosphere density and speed of sound.

    Density is returned in slug/ft^3 and speed of sound in ft/s. The equations
    match MaCa's `atmosphere.py`, including the 0 to 20 km validity range.
    """

    if altitude_m < 0.0:
        raise ValueError("altitude_m must be non-negative.")
    gravity_m_per_s2 = 9.80665
    gas_constant_j_per_kg_k = 287.058
    sea_level_pressure_pa = 101325.0
    sea_level_temperature_k = 288.15
    lapse_rate_k_per_m = 0.0065

    if altitude_m <= 11000.0:
        temperature_k = sea_level_temperature_k - lapse_rate_k_per_m * altitude_m
        pressure_pa = sea_level_pressure_pa * (
            temperature_k / sea_level_temperature_k
        ) ** (gravity_m_per_s2 / (gas_constant_j_per_kg_k * lapse_rate_k_per_m))
    elif altitude_m <= 20000.0:
        temperature_11km_k = sea_level_temperature_k - lapse_rate_k_per_m * 11000.0
        pressure_11km_pa = sea_level_pressure_pa * (
            temperature_11km_k / sea_level_temperature_k
        ) ** (gravity_m_per_s2 / (gas_constant_j_per_kg_k * lapse_rate_k_per_m))
        temperature_k = temperature_11km_k
        pressure_pa = pressure_11km_pa * exp(
            -gravity_m_per_s2
            * (altitude_m - 11000.0)
            / (gas_constant_j_per_kg_k * temperature_11km_k)
        )
    else:
        raise ValueError("Altitude out of range for MaCa atmosphere model (0-20000 m).")

    density_kg_per_m3 = pressure_pa / (gas_constant_j_per_kg_k * temperature_k)
    speed_of_sound_m_per_s = (1.4 * gas_constant_j_per_kg_k * temperature_k) ** 0.5
    return _AtmosphereState(
        density_slug_per_ft3=density_kg_per_m3 * 0.00194032,
        speed_of_sound_ft_per_s=speed_of_sound_m_per_s * 3.28084,
    )


def _required(value: float | None, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is required.")
    if not isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return value
