import unittest

from domains.constraint_analysis import (
    ConstraintAnalysisInputs,
    ConstraintAnalysisOutputs,
    ConstraintCurveResult,
    ConstraintScenarioInput,
)


def cruise_scenario() -> ConstraintScenarioInput:
    return ConstraintScenarioInput(
        name="cruise",
        beta_weight_fraction=0.9307457525779339,
        zero_lift_drag_coefficient=0.016996,
        density_slug_per_ft3=5.85189e-4,
        alpha_dry=0.27111,
        alpha_afterburner=0.332642,
        induced_drag_k1=0.116031,
        induced_drag_k2=-0.006302,
        speed_of_sound_ft_per_s=968.61,
        mach=0.87,
    )


class ConstraintAnalysisModelTests(unittest.TestCase):
    def test_constructs_maca_style_input_models(self) -> None:
        inputs = ConstraintAnalysisInputs(
            wing_loading_values_lb_per_ft2=(80.0, 100.0, 120.0),
            maximum_thrust_lb=23770.0,
            military_thrust_lb=15000.0,
            scenarios=(cruise_scenario(),),
        )

        self.assertEqual(inputs.maximum_thrust_lb, 23770.0)
        self.assertEqual(inputs.scenarios[0].name, "cruise")

    def test_rejects_empty_wing_loading_vector(self) -> None:
        with self.assertRaises(ValueError):
            ConstraintAnalysisInputs(
                wing_loading_values_lb_per_ft2=(),
                maximum_thrust_lb=23770.0,
                military_thrust_lb=15000.0,
                scenarios=(cruise_scenario(),),
            )

    def test_rejects_negative_wing_loading_value(self) -> None:
        with self.assertRaises(ValueError):
            ConstraintAnalysisInputs(
                wing_loading_values_lb_per_ft2=(80.0, -100.0),
                maximum_thrust_lb=23770.0,
                military_thrust_lb=15000.0,
                scenarios=(cruise_scenario(),),
            )

    def test_rejects_military_thrust_above_maximum_thrust(self) -> None:
        with self.assertRaises(ValueError):
            ConstraintAnalysisInputs(
                wing_loading_values_lb_per_ft2=(80.0, 100.0),
                maximum_thrust_lb=15000.0,
                military_thrust_lb=23770.0,
                scenarios=(cruise_scenario(),),
            )

    def test_rejects_afterburner_scenario_without_afterburner_lapse(self) -> None:
        with self.assertRaises(ValueError):
            ConstraintScenarioInput(
                name="takeoff",
                beta_weight_fraction=1.0,
                zero_lift_drag_coefficient=0.051996,
                density_slug_per_ft3=0.002378,
                alpha_dry=0.939778,
                use_afterburner=True,
            )

    def test_constructs_output_models(self) -> None:
        output = ConstraintAnalysisOutputs(
            wing_loading_values_lb_per_ft2=(80.0, 100.0, 120.0),
            curves=(
                ConstraintCurveResult(
                    name="cruise",
                    required_thrust_to_weight=(0.7, 0.65, 0.62),
                ),
            ),
            envelope_thrust_to_weight=(0.7, 0.65, 0.62),
            selected_wing_loading_lb_per_ft2=120.0,
            selected_thrust_to_weight=0.62,
            feasible_mask=(True, True, False),
        )

        self.assertEqual(output.curves[0].required_thrust_to_weight[1], 0.65)

    def test_rejects_curve_length_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            ConstraintAnalysisOutputs(
                wing_loading_values_lb_per_ft2=(80.0, 100.0, 120.0),
                curves=(
                    ConstraintCurveResult(
                        name="cruise",
                        required_thrust_to_weight=(0.7, 0.65),
                    ),
                ),
                envelope_thrust_to_weight=(0.7, 0.65, 0.62),
            )


if __name__ == "__main__":
    unittest.main()
