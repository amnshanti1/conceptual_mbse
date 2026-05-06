import unittest

from domains.constraint_analysis import (
    ConstraintAnalysisInputs,
    ConstraintScenarioInput,
    maca_default_constraint_inputs,
    run_constraint_analysis,
)


class ConstraintAnalysisCalculationTests(unittest.TestCase):
    def test_matches_known_maca_constraint_case(self) -> None:
        inputs = maca_default_constraint_inputs(
            beta_max_mach=0.9,
            beta_cruise=0.9307457525779339,
            beta_turn_1=0.6424006182819842,
            beta_turn_2=0.6730096890959106,
            maximum_thrust_lb=23770.0,
            military_thrust_lb=15000.0,
            wing_loading_values_lb_per_ft2=(80.0, 100.0, 120.0, 140.0, 160.0),
        )

        result = run_constraint_analysis(inputs)

        self.assertEqual(
            tuple(curve.name for curve in result.curves),
            (
                "max_mach",
                "cruise",
                "max_alt",
                "combat_turn_4_5g",
                "combat_turn_1_4g",
                "takeoff",
                "excess_powerMilSL",
                "excess_powerMil15k",
                "excess_powerMaxSL",
                "excess_powerMax15k",
            ),
        )
        self.assertEqual(
            result.wing_loading_values_lb_per_ft2,
            (80.0, 100.0, 120.0, 140.0, 160.0),
        )
        self.assertAlmostEqual(result.envelope_thrust_to_weight[0], 1.0336769639182193)
        self.assertAlmostEqual(result.envelope_thrust_to_weight[1], 0.9757726050611406)
        self.assertAlmostEqual(result.envelope_thrust_to_weight[2], 0.9377809544108041)
        self.assertAlmostEqual(result.envelope_thrust_to_weight[3], 0.91116799416432)
        self.assertAlmostEqual(result.envelope_thrust_to_weight[4], 0.891666715420244)
        self.assertAlmostEqual(result.selected_wing_loading_lb_per_ft2, 137.0334741550012)
        self.assertAlmostEqual(result.selected_thrust_to_weight, 0.91116799416432)
        self.assertAlmostEqual(
            result.landing_wing_loading_limit_lb_per_ft2, 137.0334741550012
        )
        self.assertIsNone(result.feasible_mask)
        self.assertTrue(result.assumptions)

    def test_rejects_only_landing_scenarios(self) -> None:
        inputs = ConstraintAnalysisInputs(
            wing_loading_values_lb_per_ft2=(80.0, 100.0),
            maximum_thrust_lb=23770.0,
            military_thrust_lb=15000.0,
            scenarios=(
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
            ),
        )

        with self.assertRaises(ValueError):
            run_constraint_analysis(inputs)

    def test_rejects_incomplete_generic_scenario(self) -> None:
        inputs = ConstraintAnalysisInputs(
            wing_loading_values_lb_per_ft2=(80.0, 100.0),
            maximum_thrust_lb=23770.0,
            military_thrust_lb=15000.0,
            scenarios=(
                ConstraintScenarioInput(
                    name="cruise",
                    beta_weight_fraction=0.93,
                    zero_lift_drag_coefficient=0.016996,
                    density_slug_per_ft3=5.85189e-4,
                    alpha_dry=0.27111,
                ),
            ),
        )

        with self.assertRaises(ValueError):
            run_constraint_analysis(inputs)


if __name__ == "__main__":
    unittest.main()
