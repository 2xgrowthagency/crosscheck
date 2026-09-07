# Migration and compatibility

Crosscheck is maintained by 2x Growth Agency in `2xgrowthagency/crosscheck`.
Version 0.3.0-rc.1 is a review candidate, not a release. The same organizational
repository was renamed from `independent-qa-agent`; its installed marketplace
machine identity remains `independent-qa-agent`. The visible brand is Crosscheck.

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
| Canonical skill name, instructions and references | Approved managed Crosscheck skill and four references integrated unchanged; legacy skill remains |

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
  It also accepts `crosscheck` (the default) and `independent-qa-agent`.
  These names select the same runtime package; they are not new skill aliases.

`tests/install_smoke.py` exercises all six runtime installer names, installed
CLI evaluation/receipt verification, exact canonical and legacy skill copying,
and overwrite refusal. Actual harness discovery/invocation is a separate check;
no automatic replacement of the personal plugin or new skill alias is claimed.

## Unreleased Final Boss compatibility

The distribution is now `crosscheck-verifier` and the Python package is
`crosscheck`. Use a new isolated environment instead of overwriting an old one;
no package registry replacement or automatic distribution upgrade is implied.
`final_boss` imports delegate to the same implementation. `python -m crosscheck`
and `crosscheck` write `crosscheck-receipt.json`; `python -m final_boss` and
`final-boss` retain `final-boss-receipt.json`. Both accept an explicit receipt path
and keep PASS=0, FAIL=1, BLOCKED=2 with the same validation rules.

New report headings and publication markers use Crosscheck. Receipt schema 1.1
and manifest schema 1.0 are unchanged. The old report heading is a supported
render variant, but its original byte hash and all semantic receipt fields must
still match. The schema lookup name `final-boss-receipt` remains an alias for
`crosscheck-receipt`. Approved old comment bodies remain accepted for retries;
new comments reconcile exact `final-boss-result`, `independent-qa-result` and
`workboard-qa-result` packet/target markers before updating the owned comment.

The unreleased `final-boss` marketplace entry is replaced by the available
`crosscheck` candidate entry. No released skill installation uses the old entry;
the existing `qa-agent@independent-qa-agent` entry remains available and unchanged.
Candidate availability permits isolated installation, not a release or QA PASS.

## Managed instruction source

The approved Skill Workshop package supplies
`plugins/crosscheck/skills/crosscheck/SKILL.md` and its four references:
`task-profiles.md`, `evidence-bundle.md`, `result-publication.md` and
`runtime-integration.md`. These are transferred byte-for-byte from the applied
managed source. Procedural corrections must go through the owning Workshop
flow; do not directly edit the generated package.

The canonical plugin points to `./skills/`. The Claude installer accepts the
explicit `crosscheck` name and rejects an incomplete package before writing.
Both platforms retain the legacy invocation. See the
[instruction discovery check](integrations.md#instruction-discovery) for the
separate harness acceptance boundary.

Fresh independent process QA and final owner verification remain release gates.
No live installation, merge, tag, release, personal-source archive or removal is
part of candidate preparation.
