# Synthetic evidence bundle

`current.png` was captured from the local `demo.html` at a 960 × 640 viewport.
`interaction-trace.json` records the actual ordered load/click/readback sequence
and the demo source digest. Both were reviewed before inclusion and contain only
synthetic public demo content. No personal browser profile, network headers,
cookies, customer material or private pages were used.

The manifest and receipt use simulated producer/verifier admission to demonstrate
the wire contract. The implementation worker captured the media: this is not
independent QA of Final Boss. The session clock is fixed for deterministic replay;
normal current-time validation will expire this receipt. Tests use its declared
historical evaluation time only for fixture replay, never for a real gate.

Recapture in a clean environment with Playwright 1.58.0 installed:

```bash
python scripts/capture-demo.py
```

The default Playwright Chromium must be installed, or pass `--browser` with an
explicit compatible executable. Inspect the new screenshot and trace locally,
then create a fresh manifest/session and review the exact new bytes before any
sharing. Recapturing does not automatically approve or update the stored manifest.
