"""Main application."""
from __future__ import annotations

import dataclasses
import logging
import shutil
from typing import TYPE_CHECKING

from screenshot_ocr import app_paths, google_sheets, ocr, trivia

if TYPE_CHECKING:
    import pathlib

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class AppArgs:
    """Arguments for running the application."""

    spreadsheet_id: str
    """the Google Docs spreadsheet id"""

    input_dir: pathlib.Path
    """the path to the input directory"""

    output_dir: pathlib.Path
    """the path to the output directory to move images and save text files"""

    tesseract_exe: pathlib.Path
    """the path to the tesseract executable file"""

    tesseract_data: pathlib.Path
    """the path to the tesseract data directory"""

    move_images: bool
    """whether to move processed image files"""

    google_credentials: pathlib.Path
    """the path to the Google OAuth credentials / client secrets json file"""

    google_token: pathlib.Path
    """the path to the file containing the current authorisation token data"""


class App:
    """The main application."""

    def run(self, app_args: AppArgs) -> bool:
        """Run the application.

        Args:
            app_args: The application arguments.

        Returns:
            bool: True if the application succeeded, otherwise false.
        """
        logger.info("Starting Screenshot OCR.")

        try:
            sheets_helper = google_sheets.GoogleSheetsHelper(
                app_args.google_credentials,
                app_args.google_token,
            )
            trivia_helper = trivia.TriviaHelper(sheets_helper, app_args.spreadsheet_id)
            ocr_helper = ocr.OcrHelper(
                app_args.tesseract_exe,
                app_args.tesseract_data,
            )

            input_dir = app_args.input_dir
            output_dir = app_args.output_dir
            move_images = app_args.move_images

            if not output_dir.exists():
                output_dir.mkdir(parents=True, exist_ok=True)

            count = 0

            # find the image files and extract the text from each
            for image_file in trivia_helper.find_screenshot_images(input_dir):
                output_text = ocr_helper.run(image_file) or ""
                if move_images:
                    # move the image file to the output dir
                    shutil.move(image_file, output_dir / image_file.name)

                # create a text file with the same name as the image file
                # that contains the extracted text
                output_text_file = (output_dir / image_file.stem).with_suffix(".txt")
                output_text_file.write_text(output_text)
                count += 1

                # extract the question number
                (
                    question_number,
                    question_points,
                    question_text,
                ) = trivia_helper.get_text_details(
                    output_text,
                )

                # print the image file name and extracted question number
                # and text to stdout
                logger.info(
                    '"%s": Q%s) (%s points) "%s"',
                    image_file.name,
                    question_number,
                    question_points,
                    question_text,
                )

                # update the spreadsheet cell with the text
                update_result = None
                if question_number:
                    update_result = trivia_helper.update_trivia_cell(
                        question_number,
                        question_points,
                        question_text,
                    )

                if not update_result:
                    logger.warning("Could not update spreadsheet.")

            logger.info("Finished. Found and processed %s image file(s).", count)
            return True

        except Exception as error:
            logger.exception("Error: %s - %s", error.__class__.__name__, str(error))
            return False


def build_app_args_with_defaults_from_args(**kwargs) -> AppArgs:
    """Build app arguments, using defaults for any that are missing.

    Args:
        **kwargs: The app args.

    Returns:
        An `AppArgs` instance with defaults where required.
    """
    d = app_paths.DefaultPaths()
    spreadsheet_id = kwargs.get("spreadsheet_id")
    input_dir = kwargs.get("input_dir") or d.downloads_dir
    output_dir = kwargs.get("output_dir") or d.documents_dir
    tesseract_exe = kwargs.get("tesseract_exe") or d.tesseract_exe_file
    tesseract_data = kwargs.get("tesseract_data") or d.tesseract_data_file
    google_credentials = kwargs.get("google_credentials") or d.google_credentials_file
    google_token = kwargs.get("google_token") or d.google_token_file

    move_images = kwargs.get("move_images")
    if move_images is None:
        move_images = not kwargs.get("no_move_images", False)

    logger.info("Using input directory: '%s'.", input_dir)
    logger.info("Using output directory: '%s'.", output_dir)
    logger.info("Using Tesseract executable: '%s'.", tesseract_exe)
    logger.info("Using Tesseract data: '%s'.", tesseract_data)
    logger.info("Using Google credentials: '%s'.", google_credentials)
    logger.info("Using Google token: '%s'.", google_token)

    result = AppArgs(
        spreadsheet_id=spreadsheet_id,
        input_dir=input_dir,
        output_dir=output_dir,
        tesseract_exe=tesseract_exe,
        tesseract_data=tesseract_data,
        move_images=move_images,
        google_credentials=google_credentials,
        google_token=google_token,
    )
    return result
