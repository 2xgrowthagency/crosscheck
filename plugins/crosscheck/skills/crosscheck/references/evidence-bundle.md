# Evidence bundle

## Manifest

Create `evidence-manifest.json` with schema version; packet/task; target fingerprint; base/environment; verifier execution; model/tool versions where material; capture start/end; sharing policy; criteria; checks; artifacts; hashes; skipped/inconclusive items; and invalidation triggers.

Each artifact records: stable ID, kind, path or approved URL, criterion IDs, capture time, target/environment, MIME type, byte size, SHA-256, dimensions/duration where relevant, and sharing class `local-only`, `safe-to-share`, or `redacted`.

## Media rules

- Screenshots prove visual state, not interactions or hidden persistence.
- Require current screenshots for required visual claims at named viewports.
- Require video, trace, or equivalent ordered evidence when a multi-step interaction's sequence matters.
- Keep recordings short and scoped to the criterion. Record starting state, meaningful transitions, final state, and target identity.
- Pair interaction media with persisted-state or network/readback evidence when success has a server-side effect.
- Never capture credentials, cookies, tokens, private messages, client data, or unrelated browser chrome.
- Review, crop, and redact before marking media safe to share.
- GitHub comments link only to approved durable evidence. Absolute local paths stay in the local report, never in public comments.

## Durability and freshness

Hash every artifact after capture. Re-check the target fingerprint before verdict and publication. A target mismatch or material evidence change invalidates the run. Missing required media/evidence returns BLOCKED; a captured defect returns FAIL.