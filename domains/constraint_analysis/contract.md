# Constraint Analysis Module Contract

## Purpose

The constraint analysis module evaluates conceptual aircraft performance constraints as functions of wing loading and thrust loading.

This module is intended to reuse and cleanly extract working logic from the existing MaCa project located at:

`/Users/adamshanti/MaCa`

## Initial scope

The first implementation should preserve the current working capability from MaCa as much as practical:

1. Accept wing loading ranges.
2. Accept thrust loading ranges or compute required thrust loading.
3. Evaluate constraint curves.
4. Return constraint results in a structured, testable format.
5. Support plotting later, but do not make plotting required for the core analysis.

## Inputs

The module should support typed inputs for:

1. Wing loading vector or range.
2. Thrust loading vector or range if needed.
3. Aircraft assumptions.
4. Aerodynamic assumptions.
5. Propulsion assumptions.
6. Atmosphere assumptions.
7. Takeoff constraint inputs if present.
8. Climb constraint inputs if present.
9. Cruise constraint inputs if present.
10. Dash or maneuver constraint inputs if present.
11. Landing constraint inputs if present.

## Outputs

The module should return typed outputs for:

1. Constraint names.
2. Wing loading values.
3. Required thrust loading values.
4. Feasible or infeasible mask if available.
5. Active constraint information if available.
6. Warnings or assumptions.
7. Optional plotting data, but not a plot as the primary output.

## Units

Every input and output must clearly state units.

The first extraction may preserve MaCa's existing units, but the interface must document them explicitly.

## Assumptions

The first implementation may preserve MaCa assumptions, but must document them.

Known likely assumptions include:

1. Low fidelity conceptual constraint analysis.
2. Standard atmosphere or simplified atmosphere model.
3. Constraint curves evaluated over wing loading.
4. Thrust loading used as the vertical axis or design variable.
5. Plotting should be separated from equation evaluation.

## Validation cases

The first validation case should reproduce one known MaCa constraint analysis run.

At minimum, tests should verify:

1. Constraint outputs have the same length as the wing loading vector.
2. Required thrust loading values are finite for a normal input case.
3. Invalid negative wing loading fails validation.
4. Empty wing loading vector fails validation.
5. A known MaCa baseline produces matching or close values for at least one constraint curve.

## Responsibilities

This module owns:

1. Constraint equation evaluation.
2. Constraint data preparation.
3. Feasibility masks if present.
4. Structured constraint outputs.

## Non responsibilities

This module does not own:

1. Initial takeoff weight convergence.
2. Mission segment fuel fraction tracking.
3. GUI plotting.
4. CAD geometry generation.
5. High fidelity CFD.
6. Full optimization.

## Implementation guidance for Codex

Codex should inspect `/Users/adamshanti/MaCa` and identify reusable constraint analysis logic.

Codex should not blindly copy the entire MaCa project.

Codex should separate calculations from plotting.

Codex should preserve working equations as much as practical, while wrapping them in typed inputs and outputs.

If MaCa contains several constraint scripts, Codex should summarize the candidates before choosing one.
