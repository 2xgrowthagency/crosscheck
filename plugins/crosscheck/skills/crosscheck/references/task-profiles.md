# Task profiles

Select every profile needed by the acceptance contract.

## Code and pull requests
Inputs: repo, base, exact head, PR, test/build contract, runtime boundaries.
Checks: diff/scope, focused tests, lint/type/build where relevant, regressions, dependency/config changes, exact remote/PR head.
Evidence: command results or immutable CI, diff summary, target fingerprints.
Common failures: tested wrong head, green unrelated CI, hidden scope growth, dirty/shared state.

## UI and visual work
Inputs: exact URL/revision, desktop/mobile viewports, expected states, privacy-safe accounts/data.
Checks: page load, layout, responsive behavior, overflow, content, error/empty/loading states, console and relevant network failures.
Evidence: current full-page or state-focused screenshots for required viewports, dimensions, URL/revision, capture time.
Common failures: stale screenshots, wrong preview, desktop-only proof, private information in captures.

## Interactive workflows
Inputs: starting state, ordered user journey, test identity/data, expected state transitions and side effects.
Checks: perform the flow from a clean start, verify every meaningful transition, failure/retry behavior, final persisted state, console/network errors.
Evidence: short video, Playwright trace, or equivalent sequence proof when still images cannot establish order; key-state screenshots; bounded interaction log.
Common failures: recording only the happy-path endpoint, video without target binding, unverified server-side result.
Do not require video for static changes or when it would expose secrets/private data; use a safe trace or redacted step evidence instead.

## Documents and content
Inputs: source and rendered artifact, required content, audience, links/citations, presentation rules.
Checks: meaning, completeness, hierarchy, links, citations, pagination, clipping, tables, visual consistency.
Evidence: rendered pages or safe screenshots plus source fingerprint.
Common failures: source checked without render, broken links, clipped/overflowing content, outdated facts.

## Data and reports
Inputs: source identities, ranges, timezone/currency, schema, expected transformations and totals.
Checks: completeness/pagination, schema/types, joins/formulas, null/error handling, key uniqueness, reconciliation, representative samples.
Evidence: bounded summaries, hashes, schemas, reconciliation outputs; never raw sensitive rows in public artifacts.
Common failures: truncated export, wrong account/range, unreconciled totals, hidden exclusions.

## Operations and configuration
Inputs: exact environment/account/resource, intended persisted state, safe read surfaces, mutation receipt.
Checks: stored configuration, status/logs, dry-run where applicable, live visibility separately, identifiers and observed time.
Evidence: readback receipts and bounded status output.
Common failures: config claimed from command success only, wrong environment, schedule tick mistaken for completed work.
Never mutate production merely to prove a mutation could work.

## Decisions and recommendations
Inputs: review surface, evidence snapshot, proposed action, decision owner, approval boundary.
Checks: provenance, freshness, completeness, calculations, methodology, assumptions, counterevidence, confidence, collateral risk, reversibility, protected cases, post-change verification plan.
Evidence: claim ledger and independent recomputation.
A PASS means decision-ready, never approved or authorized.

## QA process
Inputs: exact process version/config/model/tool assumptions and realistic evaluation corpus.
Checks: independence, target binding, coverage, calibration, evidence durability, privacy, publication, invalidation, rework, efficiency.
Corpus should include expected PASS, FAIL, BLOCKED, stale-target, misleading producer evidence, media requirement, privacy/redaction, and publication-failure cases.
Instruction wording alone is not behavioral proof.