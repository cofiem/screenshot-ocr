"""Features for processing screenshots and spreadsheet for online trivia."""
from __future__ import annotations

import logging
import typing
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib

    from screenshot_ocr import google_sheets

logger = logging.getLogger(__name__)


class TriviaHelper:
    """A helper for operations related to trivia screenshot images."""

    def __init__(
        self,
        sheets_helper: google_sheets.GoogleSheetsHelper,
        spreadsheet_id: str,
    ) -> None:
        """Create a new instance.

        Args:
            sheets_helper: The Google Docs spreadsheet helper.
            spreadsheet_id: The Google Docs spreadsheet identifier.
        """
        self.ss_client = sheets_helper
        self.ss_id = spreadsheet_id

    def get_number_and_question(self, value: str) -> tuple[int | None, str]:
        """Parse the question number and question text.

        Args:
            value: The raw text from the screenshot.

        Returns:
            A tuple containing the question number and text.
        """
        key_question = "question"
        number = None
        text = ""
        for line in value.splitlines():
            line_lower = line.casefold()

            if line.strip() and number is None and key_question in line_lower:
                maybe_number = line_lower.replace(key_question, "").strip()
                if maybe_number in ["il", "i1", "l1", "li", "1i", "1l", "ii"]:
                    number = 11
                else:
                    number = int(maybe_number)
                continue

            if not line.strip():
                continue
            text += " " + line.strip()

        text = text.strip()
        return number, text

    def update_trivia_cell(self, number: int, text: str) -> bool:
        """Update the Google Docs spreadsheet cell for the question number and text.

        Args:
            number: The question number.
            text: The question text.

        Returns:
            True if the cell was successfully updated, otherwise False.
        """
        first_group_start = 1
        # first_grop_end = 15
        second_group_start = 16
        second_group_end = 30

        col = "B"
        first_group_row_offset = 2
        second_group_row_offset = 5

        if not number or first_group_start > number >= second_group_end or not text:
            return False
        sheet_name = datetime.now(timezone.utc).strftime("%Y-%m-%d %a")

        row = (
            str(number + first_group_row_offset)
            if number < second_group_start
            else str(number + second_group_row_offset)
        )
        return self.ss_client.update_spreadsheet_cell(
            self.ss_id,
            sheet_name,
            col,
            row,
            text,
        )

    def find_screenshot_images(
        self,
        image_dir: pathlib.Path,
    ) -> typing.Iterable[pathlib.Path]:
        """Yield the FireFox screenshot files.

        Args:
            image_dir: The directory containing image files.

        Returns:
            An iterable of image file paths.
        """
        suffixes = [i.casefold() for i in [".png", ".jpeg", ".jpg"]]

        logger.info("Looking for screenshot images in '%s'.", image_dir)
        count = 0
        for file_path in image_dir.iterdir():
            if not file_path.is_file():
                continue
            if file_path.suffix.casefold() not in suffixes:
                continue
            if not file_path.stem.startswith("Screenshot "):
                continue

            # Screenshot 2023-10-13 at 18-45-57 Isolation Trivia Live Stream.png
            # Screenshot 2023-10-06 at 18-37-23 Facebook.png
            is_fb = "Facebook" in file_path.stem
            is_iso_triv = "Isolation Trivia" in file_path.stem
            if not is_fb and not is_iso_triv:
                continue

            count += 1
            yield file_path

        logger.info("Found %s screenshot images.", count)
