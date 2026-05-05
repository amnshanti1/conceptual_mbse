# Vision

## Long Term Vision

The long term vision is a practical conceptual fixed wing aircraft MBSE and analysis environment that helps a designer move from a rough aircraft idea to a traceable, testable, and explainable early design.

The system should support rapid design iteration without becoming a black box. A user should be able to ask:

- What mission is this aircraft sized for?
- Which assumptions drive the result?
- Which modules produced each number?
- What validity limits were reached?
- Which design variables matter most?
- How do changes in thrust loading, wing loading, aspect ratio, propulsion model, or mission profile affect the aircraft?
- Which results are verified by tests or validation cases?

The framework should feel like an engineering analysis workbench rather than a monolithic aircraft design code.

## Near Term Vision

The near term goal is a low fidelity modular Python framework for conceptual fixed wing aircraft analysis.

The first useful version should support:

- Defining an aircraft concept
- Defining a mission profile
- Running mission segment calculations
- Estimating fuel burn or energy use
- Estimating takeoff weight
- Sweeping design variables
- Producing carpet plots and fuel split plots
- Running individual domain modules independently
- Checking module assumptions and validity limits
- Verifying results against known cases

## Why This Framework Should Exist

Conceptual aircraft design often starts with many disconnected spreadsheets, scripts, textbook equations, and hand calculations. These tools are useful, but they often fail in traceability, reuse, testing, and integration.

This framework should solve those problems by making each calculation:

- Explicit
- Typed
- Tested
- Traceable
- Replaceable
- Documented
- Easy to debug

The framework should not remove engineering judgment. It should expose enough information that engineering judgment becomes easier to apply.

## User Experience Goal

The ideal user experience is:

1. Define an aircraft configuration.
2. Define a mission.
3. Choose low fidelity methods for each domain.
4. Run an integrated analysis.
5. Inspect warnings, assumptions, and intermediate values.
6. Compare design points or configurations.
7. Improve one domain module without breaking the rest of the system.

The user should be able to work at two levels:

- **Integrated workflow level**: run the full aircraft analysis loop.
- **Domain module level**: test and debug aerodynamics, propulsion, weights, or another module in isolation.

## Practical Philosophy

This project should avoid building a perfect MBSE tool too early. The practical path is:

1. Build a trustworthy low fidelity aircraft analysis kernel.
2. Enforce clean module contracts.
3. Add verification and validation discipline.
4. Add debugging and visualization tools.
5. Add higher fidelity methods only when the low fidelity framework is stable.
6. Add user interface layers after the core architecture is reliable.

## What Good Looks Like

A good result is not merely a script that produces a takeoff weight. A good result is a framework where the user can inspect why the takeoff weight changed.

A good analysis run should produce:

- Final outputs
- Intermediate outputs
- Module assumptions
- Method names
- Validity warnings
- Convergence history if applicable
- Input snapshots
- Units
- Validation status where available

## Major Domain Areas

The framework should eventually support these domains:

1. Mission analysis
2. Aerodynamics
3. Propulsion
4. Weights and mass properties
5. Performance
6. Stability and control
7. Structures
8. Geometry and packaging
9. Cost or manufacturability, if useful later
10. Requirements and trade tracking, if useful later

## CAD and Geometry Vision

The framework may eventually include basic geometry or CAD awareness, but it should not start with full CAD as the center of the system.

The near term geometry goal is lightweight geometry representation:

- Wing planform parameters
- Tail planform parameters
- Fuselage length and diameter
- Engine locations
- Fuel volume estimates
- Landing gear or payload packaging approximations
- Reference areas, spans, chords, and stations

A future CAD link should support packaging and visualization, not replace the analysis framework.

## Debugging Vision

Debugging should be a first class feature.

Future users should be able to inspect:

- Which module failed
- Which input caused failure
- Which validity limit was exceeded
- Which assumption was active
- Which intermediate value changed unexpectedly
- Which design points in a sweep failed to converge

The framework should provide plots and reports that help users understand the behavior of the design space.

## Non Goals

The first implementation is not intended to be:

- A CFD solver
- An FEA solver
- A full CAD package
- A certification tool
- A real time flight simulator
- A replacement for expert review
- A black box optimizer

