"""Command line definition."""

import logging
import pathlib

import click

from screenshot_ocr import app, utils
from screenshot_ocr.__about__ import __version__

overall_log_level = logging.DEBUG
default_app_log_level = logging.DEBUG
default_app_log_level_str = logging.getLevelName(default_app_log_level)
default_app_log_level_lower = default_app_log_level_str.lower()


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="Screenshot OCR")
@click.argument("spreadsheet_id")
@click.option(
    "--input-dir",
    type=pathlib.Path,
    help="path to the folder containing the input images",
)
@click.option(
    "--output-dir",
    type=pathlib.Path,
    help="path to the folder that " "will contain processed images and text files",
)
@click.option(
    "--tesseract-exe",
    type=pathlib.Path,
    help="path to the Tesseract executable file",
)
@click.option(
    "--tesseract-data",
    type=pathlib.Path,
    help="path to the Tesseract data directory",
)
@click.option(
    "--move-images/--no-move-images",
    default=True,
    help="move image files to the output directory " "(default true)",
)
@click.option(
    "--google-credentials",
    type=pathlib.Path,
    help="path to the Google OAuth credentials / client secrets json file",
)
@click.option(
    "--google-token",
    type=pathlib.Path,
    help="path to the file containing the current authorisation token data",
)
@click.option(
    "--log-level",
    default=default_app_log_level_lower,
    type=click.Choice(
        sorted(["debug", "info", "warning", "error", "critical"]),
        case_sensitive=False,
    ),
    help="the log level: debug, info, warning, error, critical",
)
def screenshot_ocr(
    spreadsheet_id,
    input_dir,
    output_dir,
    tesseract_exe,
    tesseract_data,
    move_images,
    google_credentials,
    google_token,
    log_level,
):
    """The spreadsheet id is the Google Docs spreadsheet id."""

    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=overall_log_level,
    )

    app_instance = app.App()

    parsed_args = {
        "spreadsheet_id": spreadsheet_id,
        "input_dir": input_dir,
        "output_dir": output_dir,
        "tesseract_exe": tesseract_exe,
        "tesseract_data": tesseract_data,
        "google_credentials": google_credentials,
        "google_token": google_token,
        "move_images": move_images,
        "no_move_images": not move_images,
        "log_level": log_level,
    }

    try:
        app_args = app.build_app_args_with_defaults_from_args(**parsed_args)

        selected_log_level = (
            parsed_args.get("log_level") or default_app_log_level_lower
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
    screenshot_ocr()
