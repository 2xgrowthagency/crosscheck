# Changelog

## 0.3.0-rc.1 — candidate, not released

Source-review rework (same unreleased candidate):
- Recheck live target, expiry and destination after lookup and delivery; return explicit stale publication state.
- Receipt schema 1.1 binds exact report bytes and criterion totals; add explicit report RISK while preserving RISKS.
- Receipt consumption requires the persisted report and preserves PASS=0, FAIL=1, BLOCKED=2.
- Manifest schema 1.0 and real screenshot/trace fixtures remain unchanged. Fresh source review and process QA are still required.

- Stage Final Boss as the 2x-owned product; preserve existing marketplace and legacy skill identity.
- Add versioned manifest/receipt schemas, deterministic evidence gate and offline CLI reports.
- Add eight profiles, current viewport proof, safe ordered trace/video requirements and privacy review binding.
- Add exact-target receipt revalidation, structured blockers/rework and separate idempotent comment publication.
- Add executable corpus, GitHub transport cases, installation smoke and Python CI matrix.
- Keep canonical skill content pending the existing Skill Workshop integration and fresh independent process QA.

## 0.1.0 — organizational baseline

Initial independent-verification skill and qa-agent plugin. The separate personal
v0.2.1 source supplies the migration behavior audited in docs/migration.md.
