# AGENTS.md

This file gives instructions to Codex and future AI coding agents working in this repository.

## Mission

Build a conceptual fixed wing aircraft MBSE and analysis framework in Python. The first goal is a low fidelity modular aircraft analysis framework, not a high fidelity simulation suite.

The framework should help an aircraft designer define a concept, run early sizing and performance analyses, compare design trades, inspect assumptions, and debug module behavior.

## Current State

This repository is a documentation only bootstrap package. Do not write implementation code until the documents in `docs/` have been read and followed.

## Required Reading Before Coding

Before making code changes, read these files:

1. `README.md`
2. `docs/vision.md`
3. `docs/architecture.md`
4. `docs/module_contract_template.md`
5. `docs/verification_strategy.md`
6. `docs/decisions/0001_core_language.md`
7. `docs/decisions/0002_module_interface_standard.md`
8. `docs/decisions/0003_initial_fidelity_strategy.md`

## Hard Rules

1. **Core language is Python.**
2. **Do not implement high fidelity methods first.**
3. **Do not create untyped module interfaces.**
4. **Do not pass loose dictionaries between domain modules unless they are explicitly wrapped, validated, or reserved for metadata.**
5. **Do not hide units.** Inputs and outputs must make units obvious.
6. **Do not write a domain module without tests.**
7. **Do not integrate a module into a workflow until it can run independently.**
8. **Do not silently extrapolate outside a method's valid range.** Raise warnings or validation errors.
9. **Do not overwrite architectural decisions without adding or updating a decision record.**
10. **Do not build a UI before the command line and module APIs are stable.**

## Design Priorities

When choosing between two implementation paths, prefer the one that is:

1. Easier to verify
2. Easier to debug
3. Easier to extend
4. Easier to explain to an aircraft designer
5. More explicit about assumptions and units

Do not optimize prematurely for performance unless a bottleneck is measured.

## Expected Future Folder Structure

When implementation begins, use this general structure unless a new decision record changes it:

```text
src/mbse/
  core/
    units/
    validation/
    registry/
    results/
    logging/
  domains/
    aerodynamics/
    propulsion/
    weights/
    performance/
    mission/
    geometry/
    stability_control/
    structures/
  workflows/
  visualization/
  io/
tests/
  unit/
  integration/
  validation/
examples/
data/
  validation/
  reference_aircraft/
```

## Module Contract Requirement

Every domain module must follow `docs/module_contract_template.md`.

At minimum, every module must define:

- Purpose
- Fidelity level
- Method name
- Typed inputs
- Typed outputs
- Units
- Assumptions
- Validity limits
- Failure modes
- Validation cases
- Unit tests
- Integration tests if used in a workflow

## Fidelity Strategy

Start with low fidelity methods that are good enough for conceptual design trades. Examples:

- Drag buildup methods
- Basic lift curve slope approximations
- Thrust lapse tables or simple lapse models
- Breguet range and endurance equations
- Segment based mission fuel fractions
- Raymer style weight estimation
- Basic takeoff and landing distance estimates
- Static margin and tail volume coefficient checks

Higher fidelity alternatives may be added later as additional methods behind the same module contract.

## Implementation Style

When code is eventually added:

- Use clear names instead of compact clever names.
- Prefer small files with narrow responsibilities.
- Prefer pure calculation functions where possible.
- Keep plotting and calculation separate.
- Keep file I/O and calculation separate.
- Include docstrings explaining equations, assumptions, and references.
- Include example inputs and expected outputs.
- Make every warning actionable.

## Testing Expectations

For every module:

- Unit tests check individual calculations.
- Contract tests check typed input and output behavior.
- Validation tests compare against known examples, textbooks, hand calculations, or reference aircraft.
- Integration tests confirm that workflows pass compatible objects between modules.

Numerical tests should use realistic tolerances and state why the tolerance is acceptable.

## Logging and Debugging Expectations

The framework should eventually support:

- Module level trace logs
- Input and output snapshots
- Assumption reports
- Validation warnings
- Workflow run summaries
- Optional debug plots
- Exportable analysis records

Debugging should be treated as a core feature, not an afterthought.

## User Interface Expectations

The first useful interface should be command line or script based. A GUI may come later.

The framework should eventually support:

- CSV or YAML mission input
- Aircraft configuration files
- Repeatable analysis runs
- Carpet plots
- Constraint plots
- Fuel split plots
- Module by module inspection
- Comparison between design cases

Do not build the GUI first.

## How to Add a New Domain Module Later

1. Create a domain folder.
2. Add a module contract document based on `docs/module_contract_template.md`.
3. Define typed input and output models.
4. Implement the lowest useful fidelity method.
5. Add assumptions and validity limits.
6. Add unit tests.
7. Add validation tests.
8. Add one standalone example.
9. Only then connect it to an integrated workflow.

## Architectural Decision Records

Important architectural changes require a new decision record in `docs/decisions/`.

Use the existing decision files as examples.

