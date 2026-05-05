# Initial Sizing Module Contract

## Purpose

The initial sizing module estimates aircraft takeoff weight and mission weight fractions from a conceptual mission profile and design variables.

This module is intended to reuse and cleanly extract working logic from the existing MaCa project located at:

`/Users/adamshanti/MaCa`

## Initial scope

The first implementation should preserve the current working capability from MaCa as much as practical:

1. Accept thrust loading input.
2. Accept wing loading input.
3. Accept aircraft and mission inputs.
4. Compute initial takeoff weight.
5. Compute fuel fraction.
6. Compute structure fraction.
7. Compute mission segment weight fractions.
8. Return traceable intermediate values.

## Inputs

The module should support typed inputs for:

1. Thrust loading, likely TSL or T/W.
2. Wing loading, likely WTOS or W/S.
3. Mission segment definitions.
4. Initial weight guess.
5. Payload weight.
6. Crew weight if applicable.
7. Fixed equipment weight if applicable.
8. Propulsion assumptions.
9. Aerodynamic assumptions needed by the existing sizing equations.
10. Fuel reserve assumptions if present in MaCa.

## Outputs

The module should return typed outputs for:

1. Converged takeoff weight.
2. Fuel weight.
3. Empty weight or structural weight fraction.
4. Fuel fraction.
5. Structure fraction.
6. Segment by segment weight fractions.
7. Segment by segment beta values if used.
8. Number of solver iterations.
9. Convergence status.
10. Warnings or assumptions.

## Units

Every input and output must clearly state units.

The first extraction may preserve MaCa's existing units, but the final interface must document them explicitly.

## Assumptions

The first implementation may preserve MaCa assumptions, but must document them in code comments or module documentation.

Known likely assumptions include:

1. Low fidelity conceptual sizing.
2. Empirical or semi empirical weight fraction methods.
3. Mission segments represented sequentially.
4. Fuel burn approximated through segment weight fractions.
5. Thrust loading and wing loading treated as design variables.

## Validation cases

The first validation case should reproduce one known MaCa run.

At minimum, tests should verify:

1. A known input case returns the same takeoff weight as MaCa within a reasonable tolerance.
2. Fuel fraction is positive and less than 1.
3. Structure fraction is positive and less than 1.
4. Mission segment fractions are ordered and traceable.
5. Invalid negative thrust loading fails validation.
6. Invalid negative wing loading fails validation.

## Responsibilities

This module owns:

1. Initial sizing calculations.
2. Weight fraction calculations.
3. Mission beta tracking when used for sizing.
4. Convergence behavior for takeoff weight.

## Non responsibilities

This module does not own:

1. Constraint diagram generation.
2. Constraint analysis equations.
3. GUI plotting.
4. CAD geometry generation.
5. High fidelity aerodynamics.
6. Engine deck interpolation.
7. Full mission simulation with time marching.

## Implementation guidance for Codex

Codex should inspect `/Users/adamshanti/MaCa` and identify reusable initial sizing logic.

Codex should not blindly copy the entire MaCa project.

Codex should extract the smallest useful amount of working logic into this module while preserving behavior.

Codex should add tests that compare against a known MaCa baseline if a clear baseline is available.

If MaCa contains multiple versions of the sizing logic, Codex should summarize the candidates before choosing one.

