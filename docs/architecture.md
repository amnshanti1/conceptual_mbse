# Architecture

## Overview

The framework should be a modular Python analysis system organized around domain modules and integrated workflows.

The core architectural idea is simple:

> Domain modules perform typed calculations. Workflows orchestrate modules. Core services handle validation, units, results, logging, and method registration.

The framework should not begin as a large application. It should begin as a reliable analysis library with clear module boundaries.

## Main Layers

### 1. Core Layer

The core layer provides shared infrastructure used by all modules.

Future responsibilities:

- Units conventions
- Type definitions
- Validation utilities
- Result containers
- Warning and error types
- Method registry
- Run metadata
- Logging and tracing
- Assumption capture
- Configuration loading

The core layer should not contain aircraft domain equations.

### 2. Domain Layer

The domain layer contains aircraft engineering modules.

Expected domain folders:

```text
src/mbse/domains/
  aerodynamics/
  propulsion/
  weights/
  performance/
  mission/
  geometry/
  stability_control/
  structures/
```

Each domain folder may contain multiple methods or fidelity levels, but all methods must follow the module interface standard.

Example domain responsibilities:

- **Aerodynamics**: lift, drag buildup, drag polar, compressibility corrections, high lift approximations.
- **Propulsion**: thrust available, fuel flow, lapse models, simple engine deck interpolation.
- **Weights**: empty weight estimates, component weight estimates, fuel or energy storage weight.
- **Performance**: climb, cruise, turn, takeoff, landing, ceiling, dash.
- **Mission**: segment definitions, segment execution, fuel fractions, convergence logic.
- **Geometry**: reference dimensions, planform calculations, packaging checks.
- **Stability and control**: static margin, tail volume coefficients, control surface sizing checks.
- **Structures**: low fidelity load paths, wing loading checks, simple bending estimates.

### 3. Workflow Layer

The workflow layer coordinates multiple domain modules into useful design analyses.

Example workflows:

- Initial sizing loop
- Mission fuel fraction analysis
- Thrust loading and wing loading sweep
- Constraint analysis
- Carpet plot generation
- Reference aircraft comparison
- Design case comparison

Workflows should be thin orchestration layers. They should not hide domain equations inside workflow code.

### 4. Visualization Layer

The visualization layer should convert results into useful plots and debug views.

Expected plots:

- Carpet plots
- Constraint plots
- Fuel split by mission segment
- Convergence history
- Sensitivity plots
- Module input/output inspection tables

Plotting must remain separate from core calculations.

### 5. I/O Layer

The I/O layer should load and save analysis definitions and results.

Potential formats:

- CSV for simple mission segment tables
- YAML or JSON for aircraft configurations
- CSV for sweep definitions
- Markdown or HTML for reports
- Parquet or CSV for large sweep outputs if needed later

I/O should validate data before it reaches domain modules.

## Data Flow

A typical integrated run should follow this pattern:

1. Load aircraft configuration.
2. Load mission definition.
3. Validate all inputs.
4. Select methods and fidelity levels.
5. Execute workflow.
6. Each workflow calls domain modules through typed contracts.
7. Each module returns typed outputs plus assumptions, warnings, and metadata.
8. Workflow gathers results into a run record.
9. Results can be plotted, exported, compared, or inspected.

## Module Interface Concept

A module should behave like a small engineering tool.

It should expose:

- A typed input model
- A typed output model
- A calculation method
- Assumptions
- Validity limits
- Validation cases
- Tests

The module should not rely on hidden global state.

## Method Registry Concept

A future method registry should allow workflows to select a method by domain, purpose, and fidelity.

Example idea:

```text
domain: aerodynamics
capability: drag_polar
method: parabolic_drag_polar
fidelity: low
```

The workflow should be able to request a capability without hard coding one implementation forever. This enables later replacement by higher fidelity methods.

## Fidelity Strategy

Each domain may eventually have several fidelity levels.

Example:

```text
aerodynamics/
  low/
    drag_buildup.py
    lift_curve_slope.py
  medium/
    vortex_lattice_adapter.py
  high/
    cfd_adapter.py
```

The first implementation should only create low fidelity methods unless a higher fidelity placeholder is needed for architecture demonstration.

## Units Strategy

The framework must make units explicit.

The first implementation can choose one internal unit system and require conversion at boundaries. Recommended internal convention:

- SI base units for internal calculations
- Explicit conversion utilities for common aerospace units
- Clear unit annotation on every input and output field

Avoid ambiguous names such as `weight`, `speed`, or `area` without units in the field name or field metadata.

## Error and Warning Strategy

Modules should distinguish between:

- Invalid input
- Out of range but still computable input
- Non convergence
- Missing required data
- Unsupported method selection
- Numerically suspicious output

A workflow should not silently continue when a critical module fails.

## Geometry Strategy

Do not make CAD the root object of the framework in the first version.

Use simple geometry objects for low fidelity analysis:

- Wing area
- Aspect ratio
- Span
- Taper ratio
- Sweep
- Mean aerodynamic chord
- Fuselage length
- Fuselage diameter
- Tail moment arm
- Engine stations
- Fuel volume estimate

Future CAD support should connect to these geometry objects rather than replacing them.

## Configuration Strategy

A future aircraft configuration should be human readable.

Potential approach:

- YAML or JSON for aircraft level definitions
- CSV for mission segment tables
- CSV or YAML for sweep variables
- Python scripts for advanced users who want direct control

The framework should support repeatable runs by saving the exact input configuration used.

## Example First Workflow

The first integrated workflow should likely be:

1. Read aircraft assumptions.
2. Read mission segments.
3. Choose low fidelity aero, propulsion, and weight methods.
4. Iterate takeoff gross weight until convergence.
5. Compute fuel or energy split by mission segment.
6. Sweep thrust loading and wing loading.
7. Generate carpet plot of converged takeoff weight.
8. Generate bar chart of fuel split by mission segment.
9. Export run summary and warnings.

## Maintainability Rules

- Keep domain equations in domain modules.
- Keep orchestration in workflows.
- Keep plotting in visualization.
- Keep file loading in I/O.
- Keep validation in core and module contracts.
- Keep tests close to the behavior they verify.

