# 0003: Initial Fidelity Strategy

## Status

Accepted

## Decision

The first implementation will use low fidelity conceptual design methods.

Higher fidelity methods may be added later, but the initial framework should prioritize simple, transparent, verifiable calculations.

## Context

The long term vision may include higher fidelity analysis, CAD linked geometry, external solvers, and richer user interfaces. However, building these first would make the system harder to verify and harder to architect cleanly.

The immediate need is a modular low fidelity framework that can perform early aircraft design trades and establish clean interfaces between domains.

## Initial Low Fidelity Methods

Candidate first methods include:

- Segment based mission analysis
- Fuel fraction or fuel burn estimation
- Breguet range and endurance equations where appropriate
- Drag buildup approximation
- Parabolic drag polar
- Simple lift curve slope approximations
- Thrust lapse model
- Basic specific fuel consumption model
- Raymer style weight estimation
- Takeoff and landing distance approximations
- Constraint analysis using thrust loading and wing loading
- Static margin and tail volume coefficient checks

## Consequences

### Positive

- Faster to build.
- Easier to test.
- Easier to explain.
- Easier to debug.
- Better for early design trades.
- Provides a stable architecture before expensive fidelity expansion.

### Negative

- Results may be approximate.
- Some configurations may not be well represented.
- Requires clear validity limits to avoid misuse.
- Higher fidelity users may eventually need additional methods.

## Implementation Guidance

Low fidelity does not mean low discipline.

Every low fidelity method still requires:

- Typed inputs
- Typed outputs
- Units
- Assumptions
- Validity limits
- Tests
- Validation cases

Higher fidelity methods should be added later as additional implementations behind the same module contract, not as replacements that break existing workflows.

