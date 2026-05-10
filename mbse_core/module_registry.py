"""Lightweight registry for domain module debugging.

The registry is intentionally declarative. It describes currently available
domain modules without changing their calculation behavior or requiring a GUI.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleEntry:
    """Debug metadata for one registered analysis module."""

    name: str
    package_path: str
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    downstream_modules: tuple[str, ...]
    status: str


REGISTERED_MODULES: tuple[ModuleEntry, ...] = (
    ModuleEntry(
        name="initial_sizing",
        package_path="domains.initial_sizing",
        purpose=(
            "Run MaCa-style low-fidelity mission fuel fraction and takeoff "
            "weight convergence."
        ),
        inputs=(
            "InitialSizingInputs",
            "InitialSizingAircraftInputs",
            "MissionSegmentInput",
        ),
        outputs=(
            "InitialSizingOutputs",
            "SegmentSizingResult",
            "converged_takeoff_weight_lb",
            "fuel_fraction",
            "structure_fraction",
        ),
        downstream_modules=("constraint_analysis",),
        status="implemented_low_fidelity",
    ),
    ModuleEntry(
        name="constraint_analysis",
        package_path="domains.constraint_analysis",
        purpose=(
            "Evaluate MaCa-style thrust-loading versus wing-loading "
            "constraint curves and select a low-fidelity design point."
        ),
        inputs=(
            "ConstraintAnalysisInputs",
            "ConstraintScenarioInput",
            "wing_loading_values_lb_per_ft2",
            "maximum_thrust_lb",
            "military_thrust_lb",
        ),
        outputs=(
            "ConstraintAnalysisOutputs",
            "ConstraintCurveResult",
            "envelope_thrust_to_weight",
            "selected_wing_loading_lb_per_ft2",
            "selected_thrust_to_weight",
        ),
        downstream_modules=(),
        status="implemented_low_fidelity",
    ),
)


def get_registered_modules() -> tuple[ModuleEntry, ...]:
    """Return registered module entries in graph display order."""

    return REGISTERED_MODULES


def get_module_entry(name: str) -> ModuleEntry:
    """Return one registered module by name."""

    for module in REGISTERED_MODULES:
        if module.name == name:
            return module
    raise KeyError(f"Unknown registered module: {name!r}.")


__all__ = [
    "ModuleEntry",
    "REGISTERED_MODULES",
    "get_module_entry",
    "get_registered_modules",
]
