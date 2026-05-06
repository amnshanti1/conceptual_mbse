import unittest

from domains.initial_sizing import (
    InitialSizingInputs,
    MissionSegmentInput,
    run_initial_sizing,
)
from tests.test_initial_sizing_models import maca_aircraft_inputs


def maca_top_level_mission_segments() -> tuple[MissionSegmentInput, ...]:
    """Mission matching `/Users/adamshanti/MaCa/mission_segments.csv`."""

    return (
        MissionSegmentInput(name="takeoff"),
        MissionSegmentInput(name="climb"),
        MissionSegmentInput(
            name="cruise", distance_nm=250.0, altitude_ft=40000.0, mach=0.85
        ),
        MissionSegmentInput(
            name="loiter", altitude_ft=35000.0, mach=0.65, endurance_min=240.0
        ),
        MissionSegmentInput(
            name="dash", distance_nm=100.0, altitude_ft=35000.0, mach=1.5
        ),
        MissionSegmentInput(name="climb"),
        MissionSegmentInput(
            name="cruise", distance_nm=400.0, altitude_ft=35000.0, mach=0.87
        ),
        MissionSegmentInput(
            name="loiter", altitude_ft=35000.0, mach=0.65, endurance_min=30.0
        ),
        MissionSegmentInput(name="landing"),
    )


class InitialSizingCalculationTests(unittest.TestCase):
    def test_matches_known_maca_top_level_mission_case(self) -> None:
        result = run_initial_sizing(
            InitialSizingInputs(
                aircraft=maca_aircraft_inputs(),
                mission_segments=maca_top_level_mission_segments(),
                convergence_tolerance_lb=10.0,
                max_iterations=250,
            )
        )

        self.assertTrue(result.converged)
        self.assertEqual(result.iterations, 70)
        self.assertAlmostEqual(result.converged_takeoff_weight_lb, 24693.90628998586)
        self.assertAlmostEqual(result.fuel_weight_lb, 10302.364035841392)
        self.assertAlmostEqual(result.empty_weight_lb, 12891.542254144468)
        self.assertAlmostEqual(result.fuel_fraction, 0.41720268615497735)
        self.assertAlmostEqual(result.structure_fraction, 0.5220535828862518)
        self.assertEqual(len(result.segment_results), 9)
        self.assertEqual(result.segment_results[-1].segment_label, "landing 1")
        self.assertAlmostEqual(result.segment_results[-1].beta_weight_fraction, 0.5829646491079579)

    def test_returns_non_converged_status_when_iteration_limit_is_too_low(self) -> None:
        result = run_initial_sizing(
            InitialSizingInputs(
                aircraft=maca_aircraft_inputs(),
                mission_segments=maca_top_level_mission_segments(),
                convergence_tolerance_lb=10.0,
                max_iterations=1,
            )
        )

        self.assertFalse(result.converged)
        self.assertEqual(result.iterations, 1)
        self.assertTrue(result.warnings)

    def test_rejects_segment_above_maca_atmosphere_range(self) -> None:
        with self.assertRaises(ValueError):
            run_initial_sizing(
                InitialSizingInputs(
                    aircraft=maca_aircraft_inputs(),
                    mission_segments=(
                        MissionSegmentInput(
                            name="cruise",
                            distance_nm=100.0,
                            altitude_ft=70000.0,
                            mach=0.85,
                        ),
                    ),
                )
            )


if __name__ == "__main__":
    unittest.main()
