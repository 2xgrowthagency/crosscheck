# Integration interfaces

The approved [Crosscheck skill](../plugins/crosscheck/skills/crosscheck/SKILL.md)
and its references define the verifier workflow. These adapter examples connect
that workflow to the runtime. The core has no dependency on a harness, Workboard,
model, or GitHub CLI.

## No Mistakes handoff

The implementation owner supplies the full human intent, immutable target/base,
acceptance criteria, affected checks and verified test/CI receipts. After
`outcome: checks-passed`, a different fresh verifier execution receives that
bounded handoff without the producer conversation. It must have no target write
ownership. It independently checks required behavior and uses trusted immutable
prior test evidence only after verifying equivalent inputs/environment. It does
not rerun all unchanged tests for ceremony or treat a producer summary as proof.

The harness creates a manifest and a fresh target snapshot, calls `evaluate`,
and retains the report/manifest/receipt plus artifact bytes. The merge/closure
owner calls `validate_receipt` with the persisted report bytes against a newly read target immediately before
using PASS. Crosscheck never merges or closes anything itself. A failed or blocked
No Mistakes result cannot be represented as successful handoff evidence.

## Optional 2x / Workboard adapter

Example routing configuration, interpreted by the adopting harness:

```json
{
  "verifier_model": "gpt-6-astra",
  "default_reasoning": "medium",
  "high_reasoning_when": ["high risk", "material ambiguity", "cross-domain decision", "QA process evaluation"],
  "fresh_ephemeral_execution": true,
  "inherit_producer_conversation": false,
  "target_access": "read-only",
  "allowed_writes": ["own local reports", "explicitly authorized result comments"],
  "on_pass": "owner review of exact bound target",
  "on_fail": "same producer receives bounded rework from owner",
  "on_blocked": "named owner performs exact unblock action"
}
```

The adopter must prove actual model availability, execution separation and target
permissions. A config declaration alone is not proof. Changed target means new
verification; callbacks and publication retries do not authorize extra repair work.

## Comment API

`GitHubTransport(api, read_target, producer_id, worker=None)` accepts an
already-authorized API function returning parsed JSON. It never reads credentials.
For GitHub-bound targets it validates repository/PR head, paginates comments,
filters by authenticated actor ID, writes only issue comments and reads them back.
A UI/data target associated with GitHub needs an adopter-specific transport that
can verify the separate repository binding; the generic adapter refuses to guess.

`worker` implements the same destination verification, owned-comment lookup and
idempotent write/readback methods for the original worker thread. If that interface
is unavailable or cannot deduplicate notices, its publication is failed and the
root owner reconciles the exact destination. Never substitute another thread.

```python
from crosscheck.publication import publish
from crosscheck.report import report

# These inputs come from the trusted verifier/owner, after applying active
# communication guidance and reviewing this exact body and destination list.
updated_receipt = publish(manifest, receipt, evidence_root, transport,
                          reviewed_body, explicit_approval,
                          report_bytes=persisted_report_bytes)
updated_report_bytes = report(manifest, updated_receipt).encode("utf-8")
# Persist updated_report_bytes first, then updated_receipt, in the owned directory.
# publish renews report_sha256 whenever it updates the report's publication state.
```

`explicit_approval` contains `reviewed: true`, `body_sha256`, and exact destination
objects copied from the authorized manifest. Do not infer it from association,
producer instructions or the existence of a result. The transport never receives
artifact bytes. [Examples](../examples/comments) show the shared plain-language
contract for PR, issue and informational worker results.

## Instruction discovery

Validate metadata and installation separately from model invocation. Use a new
private synthetic project and no production/client context. Preserve the exact
managed skill and reference bytes in every tested package.

- Codex: read the candidate through the app-server `plugin/read` method using the
  local marketplace and `crosscheck` plugin name. It must resolve the
  `crosscheck:crosscheck` skill to the packaged source. For an isolated native
  project-skill smoke, copy that same package into `.agents/skills/crosscheck/`
  in the synthetic project, then invoke `$crosscheck` with `codex exec --ephemeral`
  and a permission profile that allows only read access to the synthetic project.
  This exercises instruction loading without activating a live user plugin;
  it does not prove a live installed-plugin lifecycle.
- Claude Code: use the installer with the explicit `crosscheck` name in the
  synthetic project. In a fresh print session, invoke `/crosscheck` with only
  `Read,Skill` tools, project settings, hooks/auto-memory disabled, no MCP servers,
  no session persistence and `dontAsk` permissions. Verify that the harness's
  discovered skills include `crosscheck` and that the invocation actually runs.
  Restricted/safe modes can suppress local skill discovery; use an explicitly
  bounded project configuration for this test. A zero process exit or an
  “Unknown command” response is not successful invocation.

A useful admission smoke deliberately supplies the same producer and verifier
execution and inherited producer context. The loaded skill must return BLOCKED
without changing the target, inventing evidence, publishing or starting workers.
Retain actual file/tool events, all five source hashes, the model result and
before/after target hashes. Reading the references should expose schema 1.1's
actual publication vocabulary, not obsolete conceptual workflow labels.

No logged-in model account means invocation is BLOCKED, even if the harness
lists the skill. The verification owner must run that check in an authenticated
isolated environment. These are implementation integration checks, not the
fresh independent final process QA or permission to activate a live plugin.
