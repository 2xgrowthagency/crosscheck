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
  It also accepts `crosscheck` (the default) and `independent-qa-agent`.
  These names select the same runtime package; they are not new skill aliases.

`tests/install_smoke.py` exercises all six runtime installer names, installed
CLI evaluation/receipt verification, unchanged legacy skill copying and overwrite refusal.
App discovery of the future `$crosscheck` skill and replacement of the personal
plugin must be checked after the existing proposal is integrated. No unsupported
marketplace alias or automatic repository redirect is claimed.

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

The unavailable, unreleased `final-boss` marketplace entry is replaced by the
unavailable `crosscheck` entry. No released skill installation uses that entry;
the existing `qa-agent@independent-qa-agent` entry remains available and unchanged.

## Remaining skill source integration

The existing Skill Workshop proposal has been identified by the integration owner
and remains pending an explicit lifecycle decision. No duplicate proposal or
direct generated/installed skill edit was made. That proposal remains the
canonical source of reusable skill content; this rework changes runtime and packaging.

The integration owner must reuse that proposal to supply the canonical
`plugins/crosscheck/skills/crosscheck/SKILL.md` and the managed
`references/task-profiles.md`, `references/evidence-bundle.md`,
`references/result-publication.md` and `references/runtime-integration.md` files.
It must retain the explicit legacy invocation path and connect
those instructions to manifest 1.0 and receipt 1.1. It must establish fresh
session admission, profile selection, independent collection, exact target
readback, current media/privacy review, verdict consumption and reviewed result
publication. This is a remaining integration requirement, not a new skill proposal.

Workshop inspection does not apply or export release source. The current proposal
targets the owner's workspace skill, so its `apply` operation would write there;
it is not a repository-only export and is outside this implementation's authority.
The owner must choose an authorized managed source materialization and transfer
to the canonical repository location. Do not copy proposal front matter into a
shipped skill or hand-author substitute instructions. No activation is needed to
validate an authorized isolated package, but that package must exist first.

After managed source integration, point the canonical plugin's `skills` field to
`./skills/`, validate the plugin and skill package, and run actual isolated Codex
and Claude discovery/invocation. The Claude installer already accepts the explicit
`crosscheck` name and fails before writing when the managed package is missing.
Enable marketplace installation only after the independent owner clears the
release gates. No live installation, merge, tag, release, personal-source archive
or removal is part of this candidate preparation.
