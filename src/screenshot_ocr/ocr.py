"""Optical Character Recognition using Tesseract."""

from __future__ import annotations

import logging
import subprocess
import typing

if typing.TYPE_CHECKING:
    import pathlib

logger = logging.getLogger(__name__)


class OcrHelper:
    """OCT helper for Tesseract."""

    def __init__(self, exe_path: pathlib.Path, data_dir: pathlib.Path) -> None:
        """Create a new instance.

        Args:
            exe_path: The path to the tesseract executable.
            data_dir: The path to the tesseract data directory.
        """
        self._exe_path = exe_path
        self._data_dir = data_dir

    def run(self, image_file: pathlib.Path) -> str | None:
        """Run tesseract over an image file.

        Args:
            image_file: The path to the image file.

        Returns:
            The text from the image.
        """
        cmds = [
            str(self._exe_path),
            "--tessdata-dir",
            str(self._data_dir),
            str(image_file),
            "stdout",
        ]
        result = subprocess.run(
            cmds,
            check=True,
            capture_output=True,
            shell=False,
        )

        raw_value = result.stdout.decode(encoding="UTF-8")
        return raw_value
