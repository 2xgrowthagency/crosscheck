#!/usr/bin/env python3
"""Optional safe fixture capture. Run with Playwright installed; no personal profile."""
import argparse
import hashlib
import json
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1] / "examples" / "evidence"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", help="Optional Chromium/Chrome executable")
    args = parser.parse_args()
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 8765), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    trace = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.browser)
            page = browser.new_page(viewport={"width": 960, "height": 640})
            page.goto("http://127.0.0.1:8765/demo.html")
            for step in range(3):
                if step:
                    page.get_by_role("button", name="Check next step").click()
                actual = page.locator("output").inner_text()
                assert actual == f"Step {step} of 2"
                trace.append({"step": step, "action": "load" if step == 0 else "click Check next step",
                              "observed": actual, "captured_at": datetime.now(timezone.utc).isoformat()})
            page.screenshot(path=str(ROOT / "artifacts" / "current.png"))
            data = {"synthetic": True, "url": page.url, "browser_version": browser.version,
                    "demo_sha256": hashlib.sha256((ROOT / "demo.html").read_bytes()).hexdigest(),
                    "viewport": {"width": 960, "height": 640}, "steps": trace}
            (ROOT / "artifacts" / "interaction-trace.json").write_text(json.dumps(data, indent=2) + "\n")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
