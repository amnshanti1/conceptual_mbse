# 0001: Core Language

## Status

Accepted

## Decision

The core language for the conceptual fixed wing aircraft MBSE and analysis framework is Python.

## Context

The framework needs to support:

- Rapid engineering analysis
- Modular domain development
- Plotting and visualization
- CSV, YAML, and JSON workflows
- Scientific computing
- Testing
- Future user interfaces
- Integration with existing aerospace scripts and analysis habits

Python is well suited for this because it has strong support for numerical computing, data handling, plotting, testing, and general software architecture.

## Consequences

### Positive

- Easy to prototype conceptual design methods.
- Strong ecosystem for scientific computing.
- Good plotting support.
- Good testing tools.
- Familiar to many aerospace engineers.
- Works well for command line tools, notebooks, and future GUIs.
- Easier for Codex and other agents to modify consistently.

### Negative

- Slower than compiled languages for large numerical workloads.
- Requires discipline to avoid messy scripts.
- Requires explicit typing practices to keep interfaces clean.
- Unit handling must be designed carefully.

## Implementation Guidance

Future implementation should use Python for:

- Core package
- Domain modules
- Workflows
- Tests
- Plotting
- Configuration loading

Compiled extensions or external tools may be added later only when justified by measured need or higher fidelity integration.

