"""Low-fidelity constraint analysis calculation extracted from MaCa.

This module ports the smallest working MaCa calculation path from
`ConstraintAnalysis.py`: default scenario construction, constraint curve
evaluation, envelope calculation, and design-point selection. It intentionally
excludes CSV loading, plotting, and GUI behavior.
"""

from __future__ import annotations

from math import isfinite

from domains.constraint_analysis.models import (
    ConstraintAnalysisInputs,
    ConstraintAnalysisOutputs,
    ConstraintCurveResult,
    ConstraintScenarioInput,
)


MACA_CONSTRAINT_ASSUMPTIONS = (
    "MaCa-compatible mixed aerospace units are used internally.",
    "Constraint curves are evaluated as required takeoff thrust-to-weight over wing loading.",
    "Envelope is the pointwise maximum required thrust-to-weight across all non-landing constraints.",
    "Design wing loading is selected at minimum envelope and clamped by the landing wing-loading limit.",
    "If landing clamps the design point, selected thrust-to-weight is read from the nearest sampled wing loading.",
    "Default aerodynamic, atmosphere, lapse, runway, and excess-power values are MaCa constants.",
)


def maca_default_constraint_inputs(
    beta_max_mach: float,
    beta_cruise: float,
    beta_turn_1: float,
    beta_turn_2: float,
    maximum_thrust_lb: float,
    military_thrust_lb: float,
    wing_loading_values_lb_per_ft2: tuple[float, ...],
) -> ConstraintAnalysisInputs:
    """Build typed inputs matching MaCa's `_default_params` table."""

    return ConstraintAnalysisInputs(
        wing_loading_values_lb_per_ft2=wing_loading_values_lb_per_ft2,
        maximum_thrust_lb=maximum_thrust_lb,
        military_thrust_lb=military_thrust_lb,
        scenarios=(
            ConstraintScenarioInput(
                name="max_mach",
                alpha_dry=0.298293,
                alpha_afterburner=0.57698,
                induced_drag_k1=0.213727,
                induced_drag_k2=0.0,
                beta_weight_fraction=beta_max_mach,
                zero_lift_drag_coefficient=0.039317,
                use_afterburner=True,
                density_slug_per_ft3=0.000707,
                speed_of_sound_ft_per_s=968.61,
                mach=1.6,
            ),
            ConstraintScenarioInput(
                name="cruise",
                alpha_dry=0.27111,
                alpha_afterburner=0.332642,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.006302,
                beta_weight_fraction=beta_cruise,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=False,
                density_slug_per_ft3=5.85189e-4,
                speed_of_sound_ft_per_s=968.61,
                mach=0.87,
            ),
            ConstraintScenarioInput(
                name="max_alt",
                alpha_dry=0.138789,
                alpha_afterburner=0.17029,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.006302,
                beta_weight_fraction=0.89966,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=True,
                density_slug_per_ft3=2.98583e-4,
                speed_of_sound_ft_per_s=967.94,
                mach=0.87,
            ),
            ConstraintScenarioInput(
                name="combat_turn_4_5g",
                alpha_dry=0.555662,
                alpha_afterburner=0.681777,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.006302,
                beta_weight_fraction=beta_turn_2,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=True,
                density_slug_per_ft3=0.001265,
                speed_of_sound_ft_per_s=1036.85,
                mach=0.9,
                load_factor=4.5,
            ),
            ConstraintScenarioInput(
                name="combat_turn_1_4g",
                alpha_dry=0.357862,
                alpha_afterburner=0.556558,
                induced_drag_k1=0.219406,
                induced_drag_k2=-0.001005,
                beta_weight_fraction=beta_turn_1,
                zero_lift_drag_coefficient=0.040614,
                use_afterburner=True,
                density_slug_per_ft3=0.000707,
                speed_of_sound_ft_per_s=968.61,
                mach=1.2,
                load_factor=1.4,
            ),
            ConstraintScenarioInput(
                name="takeoff",
                alpha_dry=0.939778,
                alpha_afterburner=0.955053,
                beta_weight_fraction=1.0,
                zero_lift_drag_coefficient=0.051996,
                use_afterburner=True,
                density_slug_per_ft3=0.002378,
                maximum_lift_coefficient=1.275665,
                takeoff_speed_factor=1.2,
                runway_distance_ft=4000.0,
                rolling_friction_coefficient=0.03,
                gravity_ft_per_s2=32.2,
            ),
            ConstraintScenarioInput(
                name="landing",
                beta_weight_fraction=1.0,
                zero_lift_drag_coefficient=0.051996,
                density_slug_per_ft3=0.002378,
                maximum_lift_coefficient=1.425909,
                landing_speed_factor=1.3,
                gravity_ft_per_s2=32.2,
                rolling_friction_coefficient=0.5,
                runway_distance_ft=4000.0,
            ),
            ConstraintScenarioInput(
                name="excess_powerMilSL",
                alpha_dry=0.702727,
                alpha_afterburner=0.85355,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.0063,
                beta_weight_fraction=0.899666,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=False,
                density_slug_per_ft3=0.00237717,
                speed_of_sound_ft_per_s=1116.45,
                mach=0.9,
                velocity_ft_per_s=0.9 * 1116.45,
                load_factor=1.0,
                excess_specific_power_ft_per_s=200.0,
            ),
            ConstraintScenarioInput(
                name="excess_powerMil15k",
                alpha_dry=0.702727,
                alpha_afterburner=0.85355,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.0063,
                beta_weight_fraction=0.899666,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=False,
                density_slug_per_ft3=0.00149581,
                speed_of_sound_ft_per_s=1057.31,
                mach=0.9,
                velocity_ft_per_s=0.9 * 1057.31,
                load_factor=1.0,
                excess_specific_power_ft_per_s=50.0,
            ),
            ConstraintScenarioInput(
                name="excess_powerMaxSL",
                alpha_dry=0.702727,
                alpha_afterburner=0.85355,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.0063,
                beta_weight_fraction=0.899666,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=True,
                density_slug_per_ft3=0.00237717,
                speed_of_sound_ft_per_s=1116.45,
                mach=0.9,
                velocity_ft_per_s=0.9 * 1116.45,
                load_factor=1.0,
                excess_specific_power_ft_per_s=700.0,
            ),
            ConstraintScenarioInput(
                name="excess_powerMax15k",
                alpha_dry=0.702727,
                alpha_afterburner=0.85355,
                induced_drag_k1=0.116031,
                induced_drag_k2=-0.0063,
                beta_weight_fraction=0.899666,
                zero_lift_drag_coefficient=0.016996,
                use_afterburner=True,
                density_slug_per_ft3=0.00149581,
                speed_of_sound_ft_per_s=1057.31,
                mach=0.9,
                velocity_ft_per_s=0.9 * 1057.31,
                load_factor=1.0,
                excess_specific_power_ft_per_s=400.0,
            ),
        ),
    )


def run_constraint_analysis(inputs: ConstraintAnalysisInputs) -> ConstraintAnalysisOutputs:
    """Evaluate MaCa-style constraint curves and envelope."""

    curves: list[ConstraintCurveResult] = []
    landing_wing_loading_limit: float | None = None

    for scenario in inputs.scenarios:
        if _is_landing_scenario(scenario):
            landing_wing_loading_limit = _landing_wing_loading_limit(scenario)
            continue

        if _is_takeoff_scenario(scenario):
            curve_values = _takeoff_curve(inputs, scenario)
        else:
            curve_values = _generic_curve(inputs, scenario)
        curves.append(
            ConstraintCurveResult(
                name=scenario.name,
                required_thrust_to_weight=curve_values,
            )
        )

    if not curves:
        raise ValueError("At least one non-landing constraint scenario is required.")

    envelope = tuple(
        max(curve.required_thrust_to_weight[index] for curve in curves)
        for index in range(len(inputs.wing_loading_values_lb_per_ft2))
    )
    selected_index = min(range(len(envelope)), key=lambda index: envelope[index])
    selected_wing_loading = inputs.wing_loading_values_lb_per_ft2[selected_index]

    if (
        landing_wing_loading_limit is not None
        and isfinite(landing_wing_loading_limit)
        and selected_wing_loading > landing_wing_loading_limit
    ):
        selected_wing_loading = landing_wing_loading_limit
        selected_index = min(
            range(len(inputs.wing_loading_values_lb_per_ft2)),
            key=lambda index: abs(
                inputs.wing_loading_values_lb_per_ft2[index] - selected_wing_loading
            ),
        )

    selected_thrust_to_weight = envelope[selected_index]

    return ConstraintAnalysisOutputs(
        wing_loading_values_lb_per_ft2=inputs.wing_loading_values_lb_per_ft2,
        curves=tuple(curves),
        envelope_thrust_to_weight=envelope,
        selected_wing_loading_lb_per_ft2=float(selected_wing_loading),
        selected_thrust_to_weight=float(selected_thrust_to_weight),
        landing_wing_loading_limit_lb_per_ft2=landing_wing_loading_limit,
        feasible_mask=None,
        assumptions=MACA_CONSTRAINT_ASSUMPTIONS,
    )


def _takeoff_curve(
    inputs: ConstraintAnalysisInputs, scenario: ConstraintScenarioInput
) -> tuple[float, ...]:
    alpha = _alpha(inputs, scenario)
    beta = scenario.beta_weight_fraction
    takeoff_speed_factor = _required(scenario.takeoff_speed_factor, "takeoff_speed_factor")
    cl_max = _required(scenario.maximum_lift_coefficient, "maximum_lift_coefficient")
    gravity = _required(scenario.gravity_ft_per_s2, "gravity_ft_per_s2")
    runway_distance = _required(scenario.runway_distance_ft, "runway_distance_ft")
    rolling_friction = scenario.rolling_friction_coefficient or 0.0

    a_term = takeoff_speed_factor**2 * beta**2 / (
        alpha
        * scenario.density_slug_per_ft3
        * cl_max
        * gravity
        * runway_distance
    )
    b_term = 0.7 * scenario.zero_lift_drag_coefficient / (beta * cl_max) + rolling_friction
    return tuple(
        a_term * wing_loading + b_term
        for wing_loading in inputs.wing_loading_values_lb_per_ft2
    )


def _landing_wing_loading_limit(scenario: ConstraintScenarioInput) -> float:
    runway_distance = _required(scenario.runway_distance_ft, "runway_distance_ft")
    gravity = _required(scenario.gravity_ft_per_s2, "gravity_ft_per_s2")
    cl_max = _required(scenario.maximum_lift_coefficient, "maximum_lift_coefficient")
    landing_speed_factor = _required(
        scenario.landing_speed_factor, "landing_speed_factor"
    )
    rolling_friction = scenario.rolling_friction_coefficient or 0.0
    numerator = (
        runway_distance
        * scenario.density_slug_per_ft3
        * gravity
        * (rolling_friction * cl_max + 0.83 * scenario.zero_lift_drag_coefficient)
    )
    denominator = landing_speed_factor**2 * scenario.beta_weight_fraction
    return numerator / max(denominator, 1e-9)


def _generic_curve(
    inputs: ConstraintAnalysisInputs, scenario: ConstraintScenarioInput
) -> tuple[float, ...]:
    mach = _required(scenario.mach, "mach")
    speed_of_sound = _required(scenario.speed_of_sound_ft_per_s, "speed_of_sound_ft_per_s")
    dynamic_pressure = 0.5 * scenario.density_slug_per_ft3 * (mach * speed_of_sound) ** 2
    beta = scenario.beta_weight_fraction
    alpha = _alpha(inputs, scenario)
    k1 = _required(scenario.induced_drag_k1, "induced_drag_k1")
    k2 = scenario.induced_drag_k2 if scenario.induced_drag_k2 is not None else -0.006302
    cd0 = scenario.zero_lift_drag_coefficient

    if scenario.excess_specific_power_ft_per_s is not None:
        velocity = scenario.velocity_ft_per_s or mach * speed_of_sound
        load_factor = scenario.load_factor or 1.0
        return tuple(
            beta
            / alpha
            * (
                (dynamic_pressure / beta)
                * (1.0 / wing_loading)
                * (
                    k1 * ((load_factor * beta / dynamic_pressure) * wing_loading) ** 2
                    + k2 * ((load_factor * beta / dynamic_pressure) * wing_loading)
                    + cd0
                )
                + scenario.excess_specific_power_ft_per_s / max(velocity, 1e-9)
            )
            for wing_loading in inputs.wing_loading_values_lb_per_ft2
        )

    if scenario.load_factor is not None:
        load_factor = scenario.load_factor
        return tuple(
            beta
            / alpha
            * (
                k1 * load_factor**2 * beta / dynamic_pressure * wing_loading
                + k2 * load_factor
                + cd0 / ((beta / dynamic_pressure) * wing_loading)
            )
            for wing_loading in inputs.wing_loading_values_lb_per_ft2
        )

    return tuple(
        beta
        / alpha
        * (
            k1 * beta / dynamic_pressure * wing_loading
            + k2
            + cd0 / ((beta / dynamic_pressure) * wing_loading)
        )
        for wing_loading in inputs.wing_loading_values_lb_per_ft2
    )


def _alpha(inputs: ConstraintAnalysisInputs, scenario: ConstraintScenarioInput) -> float:
    alpha_dry = _required(scenario.alpha_dry, "alpha_dry")
    alpha_afterburner = scenario.alpha_afterburner if scenario.alpha_afterburner else 0.85
    afterburner = 1.0 if scenario.use_afterburner else 0.0
    return (
        alpha_dry * inputs.military_thrust_lb
        + afterburner
        * (alpha_afterburner * inputs.maximum_thrust_lb - alpha_dry * inputs.military_thrust_lb)
    ) / max(inputs.maximum_thrust_lb, 1e-9)


def _is_takeoff_scenario(scenario: ConstraintScenarioInput) -> bool:
    return scenario.takeoff_speed_factor is not None


def _is_landing_scenario(scenario: ConstraintScenarioInput) -> bool:
    return scenario.landing_speed_factor is not None and scenario.takeoff_speed_factor is None


def _required(value: float | None, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is required.")
    if not isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return value
