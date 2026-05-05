# Roadmap

This roadmap describes staged development from documentation to a working low fidelity conceptual aircraft analysis framework.

## Phase 0: Documentation Bootstrap

Status: current package.

Deliverables:

- Repository vision
- Architecture description
- Module contract template
- Verification strategy
- Initial architecture decision records
- Instructions for Codex and future agents

Exit criteria:

- Documentation exists.
- Core decisions are recorded.
- Implementation scope is clear.

## Phase 1: Core Skeleton

Goal: create the minimal Python package structure and shared core services.

Deliverables:

- `src/mbse/` package skeleton
- Core result object pattern
- Basic units convention
- Validation utilities
- Warning and error types
- Method metadata pattern
- Initial test structure
- Example placeholder module following the contract

Exit criteria:

- Package imports successfully.
- Tests run successfully.
- A dummy module can accept typed inputs and return typed outputs.
- No real aircraft analysis is required yet.

## Phase 2: Mission and Configuration Inputs

Goal: define the first repeatable input formats.

Deliverables:

- Aircraft configuration schema
- Mission segment schema
- Sweep definition schema
- CSV or YAML loading utilities
- Input validation tests
- Example mission file
- Example aircraft file

Exit criteria:

- A user can define a simple mission externally.
- Invalid input produces clear errors.
- Loaded inputs are converted into typed Python objects.

## Phase 3: First Low Fidelity Domain Modules

Goal: implement independently testable first pass domain modules.

Initial modules:

1. Mission segment model
2. Simple atmosphere utility
3. Aerodynamics drag polar approximation
4. Propulsion thrust lapse or engine deck approximation
5. Basic fuel flow or specific fuel consumption model
6. Weight estimation placeholder or Raymer style low fidelity estimate

Exit criteria:

- Each module has typed inputs and outputs.
- Each module has assumptions and validity limits.
- Each module has unit tests.
- Each module has at least one validation or hand calculation case.
- Each module can run independently from an example script.

## Phase 4: First Integrated Mission Analysis Loop

Goal: connect the first domain modules into a mission level analysis.

Deliverables:

- Segment based mission execution
- Fuel fraction or fuel burn per segment
- Iterative takeoff gross weight convergence
- Convergence history output
- Warnings when convergence fails
- Mission summary table

Exit criteria:

- A simple aircraft and mission can converge.
- Fuel or energy split is reported by mission segment.
- Intermediate values are inspectable.
- Integration tests cover the full workflow.

## Phase 5: Design Sweeps and Debug Plots

Goal: support early conceptual trade studies.

Deliverables:

- Thrust loading sweep
- Wing loading sweep
- Carpet plot of converged takeoff weight or fuel burn
- Fuel split bar chart
- Failure map for non converged design points
- CSV export of sweep results

Exit criteria:

- User can run a grid sweep over thrust loading and wing loading.
- Failed points are visible and explainable.
- Plots are generated from stored results, not hidden calculations.

## Phase 6: Constraint Analysis

Goal: add conceptual sizing constraints.

Candidate constraints:

- Takeoff field length
- Landing field length
- Climb rate
- Cruise thrust required
- Dash thrust required
- Service ceiling
- Sustained turn or maneuver approximation

Exit criteria:

- Constraints are modular and testable.
- Constraint plots can be generated.
- Each constraint documents assumptions and validity limits.

## Phase 7: Expanded Domain Coverage

Goal: add more low fidelity modules after the first workflow is stable.

Candidate additions:

- Static margin estimate
- Tail volume coefficient sizing
- Wing loading structural checks
- Simple wing bending moment estimate
- Fuel volume packaging check
- Engine installation and inlet loss approximations
- Basic geometry derived quantities

Exit criteria:

- New modules follow the same contract.
- Workflows can opt into new checks without breaking older analyses.

## Phase 8: Usability Layer

Goal: improve interaction without compromising core architecture.

Deliverables:

- Command line interface
- Run summary reports
- Case comparison tools
- Config templates
- Debug mode
- Optional notebook examples

Exit criteria:

- A user can run common analyses without editing package internals.
- Outputs are easy to inspect and compare.

## Phase 9: Future Fidelity Expansion

Goal: allow higher fidelity methods behind stable interfaces.

Possible additions:

- Vortex lattice or lifting line adapter
- Tabular engine deck interpolation
- Higher fidelity weight buildup
- CAD linked geometry extraction
- External tool adapters
- Optimization workflows

Exit criteria:

- Higher fidelity methods use the same input and output contracts or clearly versioned contracts.
- Low fidelity methods remain available and tested.

## Development Guidance

Do not skip phases by building a complex interface or high fidelity solver first. The framework needs a reliable low fidelity kernel before expansion.

