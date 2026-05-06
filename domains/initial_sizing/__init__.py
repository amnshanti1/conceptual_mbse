"""Initial sizing domain package."""

from domains.initial_sizing.calculation import MACA_ASSUMPTIONS, run_initial_sizing
from domains.initial_sizing.models import (
    InitialSizingAircraftInputs,
    InitialSizingInputs,
    InitialSizingOutputs,
    MissionSegmentInput,
    SegmentSizingResult,
)

__all__ = [
    "InitialSizingAircraftInputs",
    "InitialSizingInputs",
    "InitialSizingOutputs",
    "MACA_ASSUMPTIONS",
    "MissionSegmentInput",
    "SegmentSizingResult",
    "run_initial_sizing",
]
