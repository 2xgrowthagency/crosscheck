# Migration and compatibility

Final Boss is maintained by 2x Growth Agency in
`2xgrowthagency/independent-qa-agent`. Version 0.3.0-rc.1 is a review candidate,
not a release. The repository name and installed marketplace machine identity
remain stable. The visible brand is Final Boss.

The migration source is the public `jtcchan/workboard-qa-agent` commit
`d89ab5aa67f84ac695bf03c7741cfe9fb7bbb019`, whose plugin metadata declares 0.2.1.
There was no `v0.2.1` Git ref at audit time. The personal repository is untouched.

| v0.2.1 behavior | Runtime candidate disposition |
| --- | --- |
| Deliverable, decision and process modes | Preserved via eight criterion profiles and report MODE mapping |
| Immutable target/content fingerprint | Enforced by target and whole-manifest SHA-256 plus live readback input |
| Producer/verifier execution separation | Explicit admission fields, rejected self/inherited/write-owned sessions; harness attestation still required |
| Required/advisory criteria | Separate before checks; at least one required criterion; missing checks cannot pass |
| Producer claims are leads | Producer-only artifact checks cannot pass |
| Structured findings | Receipt includes criterion, observation, evidence IDs, severity, impact, disposition and owner/action |
| Stale target invalidation | Recomputed at receipt consumption and before each publication destination |
| Screenshots and interaction evidence | Strengthened to exact surface/revision/viewports and safe ordered trace/video requirements |
| Decision provenance/recalculation/counterevidence | Machine profile plus claim-ledger requirement; semantic reasoning remains fresh-verifier work |
| QA process behavioral corpus | Deterministic executed gate/CLI/publication cases; no source-text proof |
| Local technical report fields | Retained as an explicit generated-output contract |
| Plain-language publication | Reviewed summary builder plus exact-destination approval; no raw report/media upload |
| PR, issue and original worker results | Per-destination status; GitHub adapter and injected worker interface |
| Legacy publication markers | Exact packet/fingerprint matches accepted; other IDs require owner reconciliation |
| Workboard/model-specific routing | Optional adapter configuration; no universal model or orchestration dependency |
| Canonical skill name, instructions and references | Pending existing Skill Workshop proposal integration; unchanged legacy skill remains |

## Existing users

- `independent-verification`: keep the current skill. Its Claude installer copies
  the same bytes and refuses to overwrite local changes. The new runtime is an
  explicit additional installation, not a silent behavioral upgrade.
- `qa-agent@independent-qa-agent`: the original plugin path, name and skill remain.
  Marketplace display changes do not change the installed identifier.
- `workboard-qa-agent@workboard-qa-agent`: the personal installation is not edited,
  redirected or removed. Install the 2x runtime beside it with
  `./scripts/install-runtime.sh NEW_VENV workboard-qa-agent`. The same installer
  accepts `final-boss`, `independent-verification` and `qa-agent` migration names.
  These names select the same runtime package; they are not new skill aliases.

`tests/install_smoke.py` exercises all four runtime installer names, an installed
CLI/schema package, unchanged legacy skill copying and overwrite refusal.
App discovery of the future `$final-boss` skill and replacement of the personal
plugin must be checked after the existing proposal is integrated. No unsupported
marketplace alias or automatic repository redirect is claimed.

## Remaining skill source integration

This implementation lane has no callable Skill Workshop interface and could not
resolve the existing proposal’s ID through its available task/source metadata.
No duplicate proposal or direct generated/installed skill edit was made.
The existing proposal remains the canonical source of reusable skill content.

The integration owner must reuse that proposal to supply the canonical
`plugins/final-boss/skills/final-boss/SKILL.md`, companion agent metadata and mode/
publication references, retain an explicit legacy invocation path, and connect
those instructions to the version 1.0 runtime contract. It must establish fresh
session admission, profile selection, independent collection, exact target
readback, current media/privacy review, verdict consumption and reviewed result
publication. This is a remaining integration requirement, not a new skill proposal.

After integration: enable the Final Boss marketplace entry, run actual Codex and
Claude discovery/install smoke, validate plugin and skills at the new exact head,
then obtain a fresh independent process verdict. Do not release, tag, rename,
archive or remove the personal source before those gates pass.
