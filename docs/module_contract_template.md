# Module Contract Template

Every domain module must have a module contract. This file is the template for those contracts.

A module contract should be written before or alongside the implementation. Codex should use this template when creating future modules.

## Module Name

`domain.module_name`

Example:

`aerodynamics.drag_polar_low_fidelity`

## Purpose

Describe what engineering question this module answers.

Example:

> Estimate the aircraft drag polar for conceptual design using a low fidelity parabolic drag polar model.

## Domain

Choose one:

- Mission
- Aerodynamics
- Propulsion
- Weights
- Performance
- Geometry
- Stability and control
- Structures
- Other

## Fidelity Level

Choose one:

- Low
- Medium
- High
- Adapter to external tool

For the first implementation, use low fidelity unless explicitly approved by a decision record.

## Method Summary

Describe the method in plain language.

Include:

- Governing equation or conceptual model
- Main assumptions
- Expected use case
- Known limitations
- References if available

## Typed Inputs

List every required input.

| Field | Type | Units | Required | Description | Valid Range |
| --- | --- | --- | --- | --- | --- |
| example_field | float | SI units | yes | Description here | min to max |

Rules:

- Inputs must be typed.
- Units must be explicit.
- Optional inputs must have defaults or documented behavior.
- Do not use unstructured dictionaries for required engineering inputs.
- If using a nested object, document the nested object contract.

## Typed Outputs

List every output.

| Field | Type | Units | Description |
| --- | --- | --- | --- |
| example_output | float | SI units | Description here |

Rules:

- Outputs must be typed.
- Outputs must include units.
- Outputs should include enough intermediate values for debugging when useful.
- Do not return only a final scalar if intermediate values are necessary to understand the result.

## Assumptions

List all assumptions.

Example:

- Aircraft is treated as a fixed wing conventional configuration.
- Compressibility effects are ignored below the selected Mach limit.
- Drag polar is approximated as parabolic.
- Propulsion installation losses are not included.

Each assumption should be specific enough that a user can decide whether the module is appropriate.

## Validity Limits

List method limits.

Example:

| Limit | Value | Behavior if Exceeded |
| --- | --- | --- |
| Mach number | 0 to 0.8 | Warning or error |
| Angle of attack | small angle range | Warning |
| Configuration | fixed wing aircraft | Error if incompatible |

Rules:

- Validity limits must be checked where possible.
- Out of range behavior must be explicit.
- Critical invalid inputs should raise errors.
- Non critical extrapolations should raise warnings.

## Dependencies

List any dependencies on other modules or core utilities.

Example:

- Atmosphere model
- Geometry reference dimensions
- Aircraft mass properties

A domain module should not secretly load files or depend on global state.

## Failure Modes

List expected ways the module can fail.

Example:

- Missing required input
- Invalid unit conversion
- Negative wing area
- Mach number outside valid range
- Non convergence
- Incompatible aircraft configuration

For each failure mode, define whether the behavior should be:

- Error
- Warning
- Fallback
- Not allowed

## Validation Cases

Every module must include validation cases.

| Case Name | Source | Input Summary | Expected Result | Tolerance |
| --- | --- | --- | --- | --- |
| hand_calc_case_1 | Hand calculation | Brief summary | Expected value | Tolerance |

Acceptable validation sources include:

- Hand calculations
- Textbook examples
- Raymer examples
- Public reference aircraft data
- Existing trusted scripts
- Analytical limiting cases

## Unit Tests

List required unit tests.

Examples:

- Accepts valid input.
- Rejects invalid input.
- Returns expected output type.
- Preserves units convention.
- Matches hand calculation within tolerance.
- Issues warning outside validity range.

## Integration Tests

List required integration tests if this module is used in a workflow.

Examples:

- Works inside mission analysis loop.
- Compatible with geometry module outputs.
- Compatible with propulsion module outputs.
- Produces traceable warnings in run summary.

## Example Usage

Describe one minimal standalone use case.

Do not add implementation code in this documentation bootstrap. When code exists, this section may include a short code example.

## Traceability Metadata

Each module should eventually expose metadata such as:

- Module name
- Method name
- Fidelity level
- Version
- References
- Assumptions used
- Warnings generated
- Input snapshot
- Output snapshot

## Acceptance Checklist

A module is not complete until all items are checked:

- [ ] Purpose is documented.
- [ ] Fidelity level is documented.
- [ ] Inputs are typed.
- [ ] Outputs are typed.
- [ ] Units are explicit.
- [ ] Assumptions are documented.
- [ ] Validity limits are documented and checked.
- [ ] Failure modes are documented.
- [ ] Validation cases exist.
- [ ] Unit tests exist.
- [ ] Integration tests exist if used in a workflow.
- [ ] Standalone example exists.
- [ ] Warnings and errors are clear.

