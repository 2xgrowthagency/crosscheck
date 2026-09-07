"""Offline validation and report writer. Never executes commands in the target."""
import argparse
import json
import sys
from pathlib import Path

from jsonschema.exceptions import ValidationError
from .gate import evaluate, validate_receipt
from .report import report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["evaluate", "verify-receipt"])
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--current-target", type=Path, required=True,
                        help="Fresh target readback from the trusted verifier adapter")
    parser.add_argument("--target-root", type=Path, required=True,
                        help="Read-only local target root; output must be outside it")
    parser.add_argument("--output", type=Path, help="New private directory for this run")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        target = json.loads(args.current_target.read_text())
        if args.command == "verify-receipt":
            if not args.receipt:
                parser.error("verify-receipt requires --receipt")
            cleared = validate_receipt(json.loads(args.receipt.read_text()), manifest, args.evidence_root, target)
            print("PASS: exact target remains cleared" if cleared else "NON-PASS: target is not cleared")
            return 0 if cleared else 1
        if not args.output:
            parser.error("evaluate requires --output")
        output = args.output.resolve()
        if output.is_relative_to(args.target_root.resolve()) or output.is_relative_to(args.evidence_root.resolve()):
            raise ValueError("output must be outside the read-only target and evidence roots")
        receipt = evaluate(manifest, args.evidence_root, target)
        # Exclusive directory creation prevents overwriting prior evidence/results.
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
        (output / "evidence-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        (output / "qa-report.md").write_text(report(manifest, receipt))
        # Receipt is the completion marker; interrupted earlier writes never yield a gate.
        (output / "final-boss-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"{receipt['verdict']}: {receipt['meaning']}")
        return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}[receipt["verdict"]]
    except (ValidationError, ValueError, OSError):
        print("BLOCKED: invalid contract, stale receipt or unavailable safe artifact/output. Rebind inputs and use a fresh report directory.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
