# Fail-Closed AI

## Public disclosure boundary

This repository is a public inspection surface, not full architecture disclosure.

It shows a bounded claim, public language for that claim, and the claim limit.

See [`PUBLIC_DISCLOSURE_BOUNDARY.md`](PUBLIC_DISCLOSURE_BOUNDARY.md).

## What this repo is

A documentation-first public proof surface for one governance pattern:

> Invalid consequence-producing paths should fail closed rather than silently proceed.

The core question is:

> Where does the system physically stop?

## Minimal proof shape

A useful public proof surface should show:

1. what action was attempted
2. what proof was required
3. which check failed
4. whether consequence occurred
5. what receipt was written

## What this does not prove

This repository does not prove adoption, certification, standardisation, production readiness, runtime enforcement, path-universal deployment coverage, or complete AI governance.

It documents a bounded pattern and points readers to public proof objects only where each object states its own claim boundary.

## Design principles

- Stop is a first-class primitive.
- Authority is checked before mutation.
- Ambiguity fails closed.
- Receipts are written for refusal, not just success.
- Claims must be no larger than the evidence can carry.

## Boundary rule

This repository must not be read as an architecture map, orchestration model, runtime substrate, deployment model, or protected system design.

It is a public claim-surface and language anchor only.

## Status

`v0.1` — documentation-first public surface.

## Licence

MIT.
