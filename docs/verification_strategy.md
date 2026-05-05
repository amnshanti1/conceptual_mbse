# Verification Strategy

## Purpose

The verification strategy defines how this framework earns trust.

The goal is not to prove that a low fidelity conceptual design tool is perfect. The goal is to make every method transparent, bounded, tested, and traceable.

## Verification Philosophy

Every module should answer four questions:

1. Does the code implement the intended equation or method correctly?
2. Are the inputs and outputs well defined and typed?
3. Are the assumptions and validity limits explicit?
4. Does the result match known cases within an acceptable tolerance?

## Verification Levels

### 1. Unit Verification

Unit tests check small pieces of logic.

Examples:

- Equation implementation
- Unit conversion
- Input validation
- Warning generation
- Error handling
- Edge cases

Unit tests should be fast and deterministic.

### 2. Contract Verification

Contract tests check whether a module obeys the required interface.

Contract tests should verify:

- Typed input model exists.
- Typed output model exists.
- Required metadata exists.
- Assumptions are exposed.
- Validity limits are exposed.
- Invalid input is rejected.
- Output units are clear.

### 3. Validation Against Known Cases

Validation tests compare module outputs against known references.

Possible references:

- Hand calculations
- Textbook examples
- Raymer style conceptual design examples
- Public aircraft data
- Existing trusted analysis scripts
- Analytical limiting cases

Validation tests should state:

- Source of expected result
- Input values
- Expected output
- Tolerance
- Reason for tolerance

### 4. Integration Verification

Integration tests check whether modules work together.

Examples:

- Mission workflow can call aero, propulsion, and weights modules.
- Inputs passed between modules are compatible.
- Warnings propagate to the run summary.
- Convergence behavior is stable for a known case.
- A design sweep records failed and successful points correctly.

### 5. Regression Verification

Regression tests protect existing behavior.

When a method is changed, the test suite should reveal whether previous validated cases changed. If a change is intentional, update the validation documentation and explain why.

## Module Acceptance Standard

A module is acceptable for integration only after it has:

- Typed inputs
- Typed outputs
- Unit tests
- Documented assumptions
- Documented validity limits
- Validation cases
- Clear warning and error behavior
- At least one standalone example

## Workflow Acceptance Standard

A workflow is acceptable only after it has:

- A defined input schema
- A defined output schema
- Integration tests
- At least one example case
- Debug output
- Failure handling
- Run summary output

## Numerical Tolerance Guidance

Numerical tolerances should not be arbitrary.

Use tight tolerances for:

- Pure algebraic calculations
- Unit conversions
- Deterministic formulas

Use looser tolerances for:

- Iterative convergence
- Empirical correlations
- Approximate conceptual design methods
- Reference aircraft comparisons with uncertain public data

Every validation test should explain the tolerance.

## Validity Limits and Warnings

Low fidelity methods are only useful when their limits are visible.

Each module should define:

- Hard invalid ranges that produce errors
- Soft warning ranges where extrapolation is possible but risky
- Known unsupported configurations

Example behaviors:

- Negative wing area: error
- Mach number beyond model validity: warning or error depending on method
- Missing required propulsion data: error
- Extrapolated engine deck value: warning

## Assumption Tracking

Every analysis run should eventually produce an assumption record.

The record should answer:

- Which methods were used?
- Which assumptions were active?
- Which inputs were estimated?
- Which values were defaulted?
- Which warnings occurred?

This is essential for MBSE style traceability.

## Validation Data Organization

Future validation data should live in:

```text
data/validation/
```

Suggested organization:

```text
data/validation/
  aerodynamics/
  propulsion/
  weights/
  performance/
  mission/
  reference_aircraft/
```

Each validation case should include enough information to reproduce the result.

## Test Organization

Future tests should live in:

```text
tests/
  unit/
  integration/
  validation/
```

Recommended mapping:

- `tests/unit/`: small calculation tests
- `tests/integration/`: workflow and module connection tests
- `tests/validation/`: tests against reference cases

## Verification Stop Gates

Development should use stop gates.

### Module Gate

Before a module is used by a workflow:

- Contract complete
- Unit tests pass
- Validation case exists
- Standalone example runs

### Workflow Gate

Before a workflow is treated as useful:

- Input schema complete
- Output schema complete
- Integration tests pass
- Debug summary exists
- Known example runs end to end

### Release Gate

Before a version is tagged:

- Full test suite passes
- Documentation reflects current behavior
- Example cases run
- Known limitations are listed

## Handling Disagreement With Reality

Conceptual design methods often disagree with real aircraft data. That is acceptable if the disagreement is visible and understood.

When validation differs from expected values:

1. Check implementation.
2. Check units.
3. Check assumptions.
4. Check reference data quality.
5. Decide whether the method is inappropriate or the tolerance is too strict.
6. Document the outcome.

Do not tune equations blindly to match one aircraft unless the method is explicitly calibrated and documented.

