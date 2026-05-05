# 0002: Module Interface Standard

## Status

Accepted

## Decision

Every domain module must expose a typed interface with typed inputs, typed outputs, assumptions, validation cases, and tests.

A module is not complete unless it follows the contract described in `docs/module_contract_template.md`.

## Context

The framework is intended to support modular aircraft analysis across many domains. Without a strict interface standard, the project will become a collection of disconnected scripts.

The interface standard exists to make each module:

- Easy to test independently
- Easy to integrate
- Easy to debug
- Easy to replace with a higher fidelity method
- Clear about assumptions and limitations
- Traceable in an MBSE style workflow

## Required Interface Elements

Each module must define:

- Purpose
- Domain
- Fidelity level
- Method summary
- Typed inputs
- Typed outputs
- Units
- Assumptions
- Validity limits
- Dependencies
- Failure modes
- Validation cases
- Unit tests
- Integration tests if used by workflows
- Example usage

## Consequences

### Positive

- Reduces integration ambiguity.
- Makes module replacement easier.
- Supports future method registry.
- Improves debugging.
- Forces engineering assumptions to be visible.
- Makes Codex implementation safer and more consistent.

### Negative

- More upfront work for every module.
- Slower than writing quick scripts.
- Requires discipline to maintain documentation and tests.

## Implementation Guidance

Do not pass raw loose dictionaries as primary engineering inputs. Use typed models or typed data structures.

Metadata dictionaries may be acceptable for optional trace information, but required engineering inputs and outputs must be explicit.

Every module should be independently runnable before it is connected to an integrated workflow.

