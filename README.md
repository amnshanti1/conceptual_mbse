# Conceptual Fixed Wing Aircraft MBSE Framework

This repository is the bootstrap package for a conceptual fixed wing aircraft Model Based Systems Engineering and analysis framework.

The first implementation goal is a low fidelity, modular Python framework that supports early aircraft design trades. The framework should allow each aircraft domain to be developed, tested, verified, and improved independently while still integrating cleanly into a complete mission level analysis loop.

This repository currently contains documentation and implementation instructions only. No source code should be added until the architecture, module contracts, and verification approach are understood.

## Purpose

The long term goal is to build a practical conceptual aircraft design environment that combines:

- Mission analysis
- Initial sizing
- Aerodynamics
- Propulsion
- Weights and mass properties
- Performance
- Stability and control
- Structures at low fidelity
- Packaging and geometry awareness
- Debugging and visualization tools
- Traceable assumptions, requirements, and validation cases

The early goal is intentionally smaller:

> Build a low fidelity modular aircraft analysis framework in Python where each domain module has typed inputs, typed outputs, assumptions, validation cases, and tests.

## Core Principles

1. **Python first**  
   Python is the core language for orchestration, module development, analysis, testing, plotting, and future user interfaces.

2. **Low fidelity first**  
   The first working version should favor simple, transparent, verifiable methods over high fidelity simulations.

3. **Modular by domain**  
   Each major aircraft discipline should live in its own domain folder and expose a clear interface.

4. **Typed contracts**  
   Every module must define typed inputs, typed outputs, assumptions, validation cases, and tests.

5. **Independent verification**  
   A module should be testable by itself before being integrated into the main aircraft loop.

6. **Traceability over cleverness**  
   The framework should make it easy to understand where numbers came from, which assumptions were used, and which validation cases support the result.

7. **Extensibility without rewrites**  
   The architecture should allow new fidelity levels, new methods, and new features to be added without breaking existing modules.

## Intended Repository Shape

The future implementation should generally follow this structure:

```text
conceptual-mbse/
  README.md
  AGENTS.md
  docs/
    vision.md
    architecture.md
    roadmap.md
    module_contract_template.md
    verification_strategy.md
    decisions/
      0001_core_language.md
      0002_module_interface_standard.md
      0003_initial_fidelity_strategy.md
  src/
    mbse/
      core/
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
  notebooks/
```

Only the documentation folders are created in this bootstrap package.

## What Codex Should Do Later

Codex should use these documents as implementation instructions. It should not invent a new architecture unless the existing docs are updated first.

Before writing code, Codex should read:

1. `docs/vision.md`
2. `docs/architecture.md`
3. `docs/module_contract_template.md`
4. `docs/verification_strategy.md`
5. All architecture decision records in `docs/decisions/`

## Non Goals for the First Version

The first implementation should not attempt to build:

- Full aircraft CAD
- CFD
- FEA
- High fidelity propulsion cycle analysis
- Real time simulation
- Certification grade analysis
- A full graphical MBSE environment
- A large database backed application

These may become future capabilities, but the first version should focus on a trustworthy low fidelity framework.

## Documentation Map

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Instructions for Codex and future AI coding agents |
| `docs/vision.md` | Long term end state and practical design philosophy |
| `docs/architecture.md` | Proposed software architecture and module organization |
| `docs/roadmap.md` | Milestones from documentation to working framework |
| `docs/module_contract_template.md` | Required contract for every domain module |
| `docs/verification_strategy.md` | Testing, validation, and acceptance strategy |
| `docs/decisions/0001_core_language.md` | Decision record selecting Python |
| `docs/decisions/0002_module_interface_standard.md` | Decision record for typed module interfaces |
| `docs/decisions/0003_initial_fidelity_strategy.md` | Decision record for low fidelity first |

## Development Rule

No aircraft analysis module should be considered complete unless it includes:

- Typed input model
- Typed output model
- Documented assumptions
- Method description
- Units convention
- Validation cases
- Unit tests
- At least one standalone example
- Clear failure behavior
