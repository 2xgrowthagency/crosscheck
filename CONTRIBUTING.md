# Contributing

## Principles

- Preserve verifier independence: builder claims are inputs, not proof.
- Preserve read-only defaults and explicit authorization boundaries.
- Keep `PASS`, `FAIL`, and `BLOCKED` mutually exclusive.
- Prefer observable checks and immutable identifiers over narrative confidence.
- Keep product repair, merge, deploy, and publication outside the QA verdict.

## Pull requests

1. Explain the QA failure mode the change addresses.
2. Add or update a representative packet in `examples/`.
3. Run `python3 tests/validate.py`.
4. Validate the Codex plugin with the current plugin validator.
5. Confirm that no private paths, credentials, client data, or internal queue details were added.
