# Contributing

Keep target verification separate from implementation and release authority.
Changes must preserve exact binding, fresh execution, independent proof,
required/advisory criteria, safe media, bounded rework and publication separation.

## Pull requests

Explain the concrete failure mode and resulting behavior. Preserve the original
human intent verbatim when supplied by the source issue. Describe tested behavior,
compatibility, remaining integration requirements and residual risks. Keep the
release candidate PR in draft until the independent owner completes the gates.

Run `python tests/validate.py`, `python -m unittest discover -s tests -v`,
`python tests/install_smoke.py`, and `git diff --check` with requirements installed.
Validate both plugins with the current Codex plugin validator and every shipped
skill with the current skill validator. Tests must execute contracts and behavior;
source-string or prompt-keyword checks are not behavioral proof.

The CI workflow runs on pull requests and pushes to main across supported Python
versions. The baseline has no initialized No Mistakes configuration; when that
remains true, run the authorized standalone review after tests and report the
initialization blocker precisely. Do not invent a no-CI exemption.

## Release gate

Version 0.3.0-rc.1 stages runtime/schema/packaging work. The existing canonical
Skill Workshop proposal must be integrated by its owner before enabling the new
skill/plugin. Do not directly edit or install generated skill content in this lane.

A separate fresh, read-only verifier must evaluate the exact candidate head,
including live harness separation, profile reasoning, media/privacy behavior,
publication retries, actual plugin discovery and legacy migration. It must not
be the implementation worker. Tests and source review are implementation proof,
not independent QA. Any head change invalidates prior exact-head QA.

Only the release owner may authorize readiness, merge, tag, release, repository
rename or personal-source archival. No such action is part of candidate preparation.
Do not include private paths, credentials, client data or unreviewed media in GitHub.
