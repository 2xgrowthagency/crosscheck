# Runtime contracts: manifest 1.0, receipt 1.1

The JSON schemas shipped inside `final_boss/schemas/` are the authoritative wire
shapes. Unknown fields, unsupported versions, malformed identifiers/timestamps,
missing fields, duplicate IDs and dangling check references are rejected.
Schema validation establishes shape. Runtime evaluation additionally establishes
hash, time, coverage and verdict invariants. Neither can establish agent honesty.

## Evidence manifest

- `target` binds kind, stable locator, exact revision/content hash, base/expected
  state, environment and configuration digest. `fingerprint(target)` is SHA-256
  over UTF-8 JSON sorted by key with compact separators and unescaped Unicode.
  Timestamps alone are not identity. A code adapter compares local/remote/PR heads;
  mutable issue, recommendation, data and configuration adapters hash all material
  content into revision/configuration fields. Decision binding includes review
  content, underlying sources and proposed action. Process binding includes
  package, tool/model configuration and evaluated corpus. URL alone is insufficient.
- `session` records producer/verifier identities, start/finish, ephemeral execution,
  inherited context, target write ownership/writes and separation attestation.
  A producer may supply leads; the trusted harness supplies these admission facts.
  Same model or human is allowed; same producer execution is not.
- `criteria` classifies required/advisory checks before observation. At least one
  criterion is required. `profile`, `visual`, `sequence` and `viewports` encode
  the evidence requirements; the full manifest hash freezes this contract.
- `checks` maps each observation to a criterion and artifact IDs, with pass/fail/
  blocked, an exact next action and owner. Multiple checks for a required criterion
  must all conclude. Required defects cannot be downgraded to advisory findings.
- `artifacts` records relative paths, SHA-256, size, kind, origin, verifier session,
  target fingerprint, capture time, tool/version, media surface/revision/viewport,
  sharing class, and privacy review of the exact bytes. Capture must fall within
  the bound session. Files must stay in the bundle, without symlinks/traversal.
  Producer artifacts may remain as leads; they cannot establish a required check.
- `freshness_seconds` expires the run from session finish. Future captures, changed
  bytes, changed targets and expired sessions invalidate the run.
- `destinations` lists every explicitly associated PR, issue and original worker
  thread separately. Association is not authorization. Each has its own exact
  locator and `authorized` flag. No discovery or expansion occurs in the runtime.

## Evidence policy

Every required passing check needs independent artifacts of its profile’s type.
UI checks and any visual claim require current screenshots for every declared
viewport at the exact bound locator and revision. Document checks require rendered
proof; visual document claims additionally use screenshots with page/view identity
encoded by the adapter. Data requires reconciliation; operations require persisted
readback; decisions require a claim ledger; process targets require executed cases.
Console/network/HTTP logs are supplementary when relevant to the criteria.

A material ordered interaction with `sequence: true` requires a video or trace
whose observed sequence is explicitly established at the bound surface/revision.
Stills alone cannot clear it. Static and nonvisual work does not require video.
A trace can record ordered safe actions and readbacks without capturing raw network
headers, cookies or screen content. If no safe proof exists, return BLOCKED with
an exact safe-surface/unblock request; never force unsafe recording.

`local-only` evidence can prove behavior without publication review. A
`safe-to-share` or `redacted` declaration requires an approved review whose hash
matches the exact sanitized bytes. Classification does not upload anything.
Redaction changes the evidence: hash and review the sanitized derivative and bind
it in a fresh manifest/session. No automatic detector can certify privacy.

## Gate receipt and report

`final-boss-receipt.json` binds packet, exact target, full manifest, verifier,
evaluation/expiry, verdict, practical meaning, structured problems and per-destination
publication status. Problems identify criterion, observation, evidence IDs, severity,
impact, owner, disposition and bounded action. Only PASS has `gate_cleared: true`.

Receipt 1.1 adds required `report_sha256` and `criterion_totals`. This is an
intentional pre-release contract change: 1.0 receipts must be regenerated from
their original evidence at a valid historical fixture time, or replaced by a
fresh real verification. Old receipts cannot clear the new gate. Manifest and
target schema versions remain unchanged.

`criterion_totals` separates required and advisory criteria, each with `total`,
`passed`, `failed` and `blocked` counts. Each criterion is counted once, regardless
of how many checks it has. Missing or inconclusive checks count as blocked;
independent defects take precedence over missing proof for that criterion.
Global target/session/evidence invalidation marks every criterion blocked.
Advisory outcomes never change the required verdict. Consumption recomputes all
counts from evidence; a schema-valid but fabricated total cannot pass.

An invalid target/session or evidence-integrity/privacy condition takes precedence
as BLOCKED. Otherwise an independently observed required defect gives FAIL even if
another check is incomplete. Missing proof gives BLOCKED. Advisory limitations
remain in the report and cannot excuse a required defect.

`validate_receipt` recomputes the outcome from current target and artifact bytes;
it requires persisted `report_bytes` and rejects altered manifests, mismatched
reports and expired/forged receipts. Consumers must use this
operation at the gate. Hashes provide binding, not signatures or authentication.
The caller must protect the receipt, criteria and readback sources from producers.
Any push, rebase, deployment, evidence refresh, material config/tool change or
expired session requires a fresh verifier run. There is no automatic repair loop.

`qa-report.md` retains the v0.2.1 field names, including RESULT, MODE, SCOPE, INTENT,
INDEPENDENCE, TARGET_FINGERPRINT, EVIDENCE_SNAPSHOT, CRITERIA_MATRIX, FINDINGS,
INDEPENDENT_CHECKS, EVIDENCE, ARTIFACTS, SKIPPED_OR_INCONCLUSIVE, RISK, RISKS,
INVALIDATION_TRIGGERS, PUBLICATION and RECOMMENDATION. It is a local technical
record. Human summaries are separate reviewed text.

The report includes `CRITERION_TOTALS` and an explicit `RISK` field; `RISKS`
remains a compatibility alias. Render the report as exact UTF-8 bytes, then hash
those bytes into the receipt. The report never renders `report_sha256` or a hash
of the receipt, so the dependency is not circular. `bind_report` renews this
binding after publication statuses change. Consumption checks both the persisted
bytes' digest and their match to the canonical render of the supplied manifest
and receipt. Modified, missing, swapped and mixed-generation reports fail closed.
Persist the regenerated report first and its receipt last. An interruption between
these writes cannot turn mismatched generations into a valid completion packet.

## Result publication

`publication.publish` accepts a trusted comment transport and an exact reviewed
body plus explicit destination approval. It sends only that body, never artifact
bytes, raw reports or transport exceptions. Apply the caller’s active communication
guidance at response time, then approve the resulting bytes. No private guidance
is copied into this project. Approval may be supplied by an authorized owner or
adapter under the task’s sharing policy; it is never inferred from elapsed time.

Summaries explain the ticket purpose, checks, verdict meaning, failure/blocker,
next owner/action and whether a human needs to act. A worker notice is informational,
not a repair dispatch. FAIL is routed by the owner to one bounded repair assignment;
a changed target receives a fresh verifier. BLOCKED names the exact unblock owner/action.

The stable marker binds packet plus target digest. The publisher searches owned
comments, skips identical text, updates changed text and reconciles after timeouts.
The GitHub transport paginates all comments and checks immutable author ID. Older
`independent-qa-result` and `workboard-qa-result` markers are recognized when their
packet/target IDs exactly match the new fingerprint. Other historical marker
identities need explicit owner reconciliation, never guessed conversion.

One publisher owns a packet/target window. No service-side conditional comment
creation exists in this adapter: competing writers require external serialization.
After remote discovery, immediately before writing or reusing a comment, and after
transport readback, the publisher rechecks destination binding, live target and
current time/expiry. Its clock is sampled after remote work; the old fixed `now`
argument has been replaced by a callable `clock` for deterministic tests only.
A known-stale result returns BLOCKED with `stale` publication status and preserves
any returned comment location for owner reconciliation. It does not automatically
send an unreviewed replacement message or claim current publication success.

These checks cannot atomically lock a remote target against a concurrent push or
deployment. A mutation after the last read, or a write/readback timeout, may still
leave a stale remote comment. Owners reconcile using the bound marker and recorded
location; gate consumers must always reread the target and validate the exact
receipt/report/evidence packet. A comment is never the clearance authority.

A transport failure records `failed` and leaves a conclusive verdict
unchanged. A required-publication workflow remains incomplete until every required
destination succeeds, even if the product verdict is PASS. Persist the returned
regenerated report and renewed publication receipt locally; never retry from only a cached
success flag. Comment text is informational and must never substitute for a fresh gate.
