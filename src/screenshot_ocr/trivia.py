"""Features for processing screenshots and spreadsheet for online trivia."""
from __future__ import annotations

import logging
import re
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

    def get_text_details(self, value: str) -> tuple[int | None, int | None, str]:
        """Parse the question text to get the number, points, and question text.

        Args:
            value: The raw text from the screenshot.

        Returns:
            A tuple containing the question number, points, and text.
        """
        # output
        number = None
        points = 1
        text = ""

        # initial
        fixes = {
            "i": "1",
            "l": "1",
            "o": "0",
        }
        num_map = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
        }
        key_question = "question"
        re_points = re.compile(r"(?P<num>(one|two|three|four|five))\s+points?")

        for line in value.splitlines():
            line_strip = line.strip()
            if not line_strip:
                continue

            line_lower = line_strip.casefold()

            if key_question in line_lower and not number:
                start_index = line_lower.index(key_question) + len(key_question)
                raw = list(line_lower[start_index:].strip())

                for index, char in enumerate(raw):
                    if char in fixes:
                        raw[index] = fixes[char]

                number_raw = "".join(raw)
                if all(c.isdigit() for c in number_raw):
                    number = int(number_raw)
                    continue

            match = re_points.search(line_lower)
            if match and points == 1:
                num_word = match.group("num")
                points = num_map[num_word]

            text += " " + line.strip()

        text = text.strip()
        return number, points, text

    def update_trivia_cell(self, number: int, points: int, text: str) -> bool:
        """Update the Google Docs spreadsheet cell for the question number and text.

        Args:
            number: The question number.
            points: The points for the question.
            text: The question text.

        Returns:
            True if the cell was successfully updated, otherwise False.
        """
        first_group_start = 1
        # first_grop_end = 15
        second_group_start = 16
        second_group_end = 30

        col_text = "B"
        col_points = "D"
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
        result_text = self.ss_client.update_spreadsheet_cell(
            self.ss_id,
            sheet_name,
            col_text,
            row,
            text,
        )
        result_points = self.ss_client.update_spreadsheet_cell(
            self.ss_id,
            sheet_name,
            col_points,
            row,
            str(points),
        )
        return result_text and result_points

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
