"""Command line for screenshot ocr."""

from __future__ import annotations

import argparse
import logging
import pathlib
import sys

from screenshot_ocr import app, utils


def main(args: list[str] | None = None) -> int:
    """Run as a command line program.

    Args:
        args: The program arguments.

    Returns:
        int: Program exit code.
    """
    if args is None:
        args = sys.argv[1:]

    overall_log_level = logging.DEBUG
    default_app_log_level = logging.DEBUG
    default_app_log_level_str = logging.getLevelName(default_app_log_level)
    default_app_log_level_lower = default_app_log_level_str.lower()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=overall_log_level,
    )

    parser = argparse.ArgumentParser(
        prog="screenshot-ocr",
        description="Extract text from screenshots.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {utils.get_version()}",
    )
    parser.add_argument(
        "spreadsheet_id",
        help="the Google Docs spreadsheet id",
    )
    parser.add_argument(
        "--input-dir",
        type=pathlib.Path,
        help="path to the folder containing the input images",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="path to the folder that will contain processed images and text files",
    )
    parser.add_argument(
        "--tesseract-exe",
        type=pathlib.Path,
        help="path to the Tesseract executable file",
    )
    parser.add_argument(
        "--tesseract-data",
        type=pathlib.Path,
        help="path to the Tesseract data directory",
    )
    parser.add_argument(
        "--no-move-images",
        action="store_true",
        help="don't move image files to the output directory "
        "(image files are moved by default)",
    )
    parser.add_argument(
        "--google-credentials",
        type=pathlib.Path,
        help="path to the Google OAuth credentials / client secrets json file",
    )
    parser.add_argument(
        "--google-token",
        type=pathlib.Path,
        help="path to the file containing the current authorisation token data",
    )
    parser.add_argument(
        "--log-level",
        default=default_app_log_level_lower,
        choices=["debug", "info", "warning", "error", "critical"],
        help="the log level: debug, info, warning, error, critical",
    )

    parsed_args = parser.parse_args(args)

    app_instance = app.App()

    try:
        app_args = app.build_app_args_with_defaults_from_args(**vars(parsed_args))

        selected_log_level = (
            parsed_args.log_level or default_app_log_level_lower
        ).upper()
        logging.getLogger().setLevel(selected_log_level)

        result = app_instance.run(app_args)
        if result is True:
            return 0

        return 1

    except utils.ScreenshotOcrError as error:
        utils.log_exception(error)
        return 1

    except Exception as error:  # noqa: BLE001
        # Catch broad exception to log error.
        utils.log_exception(error)
        return 2


if __name__ == "__main__":
    sys.exit(main())
