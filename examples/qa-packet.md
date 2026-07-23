# QA packet

## Identity

- Packet ID: `example-001`
- Builder: `<builder task or agent>`
- Verifier: separate from builder

## Immutable target

- Repository or artifact: `<path or URL>`
- Base revision: `<commit or expected state>`
- Target revision: `<commit, artifact hash, or deployment ID>`

## Acceptance criteria

1. `<observable criterion>`
2. `<observable criterion>`
3. `<observable criterion>`

## Required lanes

- [ ] Code
- [ ] Browser and UI
- [ ] Documents
- [ ] Data artifacts
- [ ] Operational proof

## Authorized surfaces

- Paths: `<exact paths>`
- URLs: `<exact URLs>`
- Commands: `<allowed commands or command classes>`
- Interactions: `<safe test interactions>`

## Evidence and sharing

- Artifact directory: `<local directory>`
- Sharing policy: `local-only | redacted-summary-ok | explicitly-public`
- Result publication: `not-authorized | authorized to <exact destination>`

## Stop conditions

- Return `BLOCKED` if: `<missing input, unsafe surface, auth requirement, or capability>`
- Do not: `<product mutations or out-of-scope access>`

## Requested output

Use the `independent-verification` skill and return the exact QA report contract with one verdict: `PASS`, `FAIL`, or `BLOCKED`.
