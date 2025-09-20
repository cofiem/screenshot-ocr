"""Main entry point."""

import sys

if __name__ == "__main__":
    from screenshot_ocr.cli import screenshot_ocr

    sys.exit(screenshot_ocr())
