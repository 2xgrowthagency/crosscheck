"""Keep the unreleased CLI name and receipt filename as compatibility aliases."""
import sys
from crosscheck.__main__ import main as crosscheck_main


def main():
    return crosscheck_main(receipt_name="final-boss-receipt.json")


if __name__ == "__main__":
    sys.exit(main())
