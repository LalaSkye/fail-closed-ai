# Repository Receipt

Date: 2026-05-11
Repository: `LalaSkye/fail-closed-ai`
Evidence class: documentation-first reference / bounded artefact / design and test-artifact support surface

## Object

`fail-closed-ai` is a documentation-first reference for AI systems that stop before unsafe consequence.

It describes the fail-closed execution-control pattern and links it to executable proof surfaces where implementation exists.

## What this repository does

- Defines the fail-closed AI boundary pattern.
- States the governance corridor from proposal to consequence and receipt.
- Defines core concepts including admissibility, authority, scope, freshness, replay, and receipt evidence.
- Points to executable kernels and related proof surfaces where available.
- Provides a bounded documentation anchor for design and test artefacts.

## What this repository does not do

This repository does not claim:

- adoption
- certification
- compliance
- endorsement
- production readiness
- field validation
- standardisation
- runtime enforcement by itself
- path-universal deployment coverage
- that every AI risk can be solved by one gate

## Proof surface

Useful inspection questions:

1. What action is being proposed?
2. What authority is required?
3. Is the action scoped, fresh, unreplayed, and admissible?
4. Where does execution stop when proof is missing?
5. Was consequence prevented?
6. What receipt records the refusal?

## Related evidence

- Executable kernel: `LalaSkye/commit-gate-core`
- Consequence-control documents: `docs/` where present
- Reference schemas: `reference/` where present

## Claim boundary

Allowed claim:

> This repository documents a bounded fail-closed execution-control pattern: AI-controlled actions should not become consequence unless required proof is present at the boundary where consequence occurs.

Not allowed:

> This repository proves adoption, compliance, certification, production readiness, runtime enforcement, or path-universal governance coverage.

## Receipt line

A policy may describe a rule. A fail-closed system must show where invalid consequence stops.
