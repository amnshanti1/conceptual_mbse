import unittest

from domains.initial_sizing import (
    InitialSizingAircraftInputs,
    InitialSizingInputs,
    InitialSizingOutputs,
    MissionSegmentInput,
    SegmentSizingResult,
)


def maca_aircraft_inputs() -> InitialSizingAircraftInputs:
    return InitialSizingAircraftInputs(
        fixed_weight_lb=1500.0,
        initial_takeoff_weight_guess_lb=30000.0,
        wing_loading_lb_per_ft2=130.0,
        thrust_to_weight_ratio=1.1,
        cruise_drag_coefficient=0.016996,
        cruise_tsfc_per_s=0.00016,
        loiter_drag_coefficient=0.019,
        loiter_tsfc_per_s=0.00019,
        dash_drag_coefficient=0.019,
        dash_tsfc_per_s=0.00061,
        oswald_efficiency=0.91443,
        wing_aspect_ratio=3.0,
    )


class InitialSizingModelTests(unittest.TestCase):
    def test_constructs_maca_style_input_models(self) -> None:
        inputs = InitialSizingInputs(
            aircraft=maca_aircraft_inputs(),
            mission_segments=(
                MissionSegmentInput(name="takeoff"),
                MissionSegmentInput(
                    name="cruise", distance_nm=250.0, altitude_ft=40000.0, mach=0.85
                ),
                MissionSegmentInput(
                    name="loiter", altitude_ft=35000.0, mach=0.65, endurance_min=240.0
                ),
                MissionSegmentInput(
                    name="dash", distance_nm=100.0, altitude_ft=35000.0, mach=1.5
                ),
                MissionSegmentInput(name="landing"),
            ),
        )

        self.assertEqual(inputs.aircraft.wing_loading_lb_per_ft2, 130.0)
        self.assertEqual(len(inputs.mission_segments), 5)

    def test_rejects_negative_wing_loading(self) -> None:
        with self.assertRaises(ValueError):
            InitialSizingAircraftInputs(
                fixed_weight_lb=1500.0,
                initial_takeoff_weight_guess_lb=30000.0,
                wing_loading_lb_per_ft2=-130.0,
                thrust_to_weight_ratio=1.1,
                cruise_drag_coefficient=0.016996,
                cruise_tsfc_per_s=0.00016,
                loiter_drag_coefficient=0.019,
                loiter_tsfc_per_s=0.00019,
                dash_drag_coefficient=0.019,
                dash_tsfc_per_s=0.00061,
                oswald_efficiency=0.91443,
                wing_aspect_ratio=3.0,
            )

    def test_rejects_negative_thrust_loading(self) -> None:
        with self.assertRaises(ValueError):
            InitialSizingAircraftInputs(
                fixed_weight_lb=1500.0,
                initial_takeoff_weight_guess_lb=30000.0,
                wing_loading_lb_per_ft2=130.0,
                thrust_to_weight_ratio=-1.1,
                cruise_drag_coefficient=0.016996,
                cruise_tsfc_per_s=0.00016,
                loiter_drag_coefficient=0.019,
                loiter_tsfc_per_s=0.00019,
                dash_drag_coefficient=0.019,
                dash_tsfc_per_s=0.00061,
                oswald_efficiency=0.91443,
                wing_aspect_ratio=3.0,
            )

    def test_rejects_missing_cruise_distance(self) -> None:
        with self.assertRaises(ValueError):
            MissionSegmentInput(name="cruise", altitude_ft=40000.0, mach=0.85)

    def test_rejects_empty_mission(self) -> None:
        with self.assertRaises(ValueError):
            InitialSizingInputs(aircraft=maca_aircraft_inputs(), mission_segments=())

    def test_constructs_output_models(self) -> None:
        output = InitialSizingOutputs(
            converged_takeoff_weight_lb=24693.9,
            fuel_weight_lb=10302.4,
            empty_weight_lb=12891.5,
            fuel_fraction=0.42,
            structure_fraction=0.52,
            segment_results=(
                SegmentSizingResult(
                    segment_label="takeoff 1",
                    fuel_burn_lb=494.1,
                    beta_weight_fraction=0.98,
                ),
            ),
            iterations=70,
            converged=True,
        )

        self.assertTrue(output.converged)
        self.assertEqual(output.segment_results[0].segment_label, "takeoff 1")

    def test_rejects_invalid_output_fraction_sum(self) -> None:
        with self.assertRaises(ValueError):
            InitialSizingOutputs(
                converged_takeoff_weight_lb=24693.9,
                fuel_weight_lb=10302.4,
                empty_weight_lb=12891.5,
                fuel_fraction=0.6,
                structure_fraction=0.5,
            )


if __name__ == "__main__":
    unittest.main()
