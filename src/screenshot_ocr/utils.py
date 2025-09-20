"""Small utility functions."""

from __future__ import annotations

import logging

from importlib_metadata import PackageNotFoundError, distribution
from importlib_resources import as_file, files

logger = logging.getLogger(__name__)


def get_name_dash() -> str:
    """Get the package name with word separated by dashes."""
    return "screenshot-ocr"


def get_name_under() -> str:
    """Get the package name with word separated by underscores."""
    return "screenshot_ocr"


def get_author_dash() -> str:
    """Get the package author with word separated by dashes."""
    return "anotherbyte-net"


def get_author_under() -> str:
    """Get the package author with word separated by underscores."""
    return "anotherbyte_net"


def get_version() -> str | None:
    """Get the package version."""
    try:
        dist = distribution(get_name_dash())
        return dist.version
    except PackageNotFoundError:
        pass

    try:
        with as_file(files(get_name_under()).joinpath("cli.py")) as file_path:
            version_text = (file_path.parent.parent.parent / "VERSION").read_text()
            return str(version_text.strip())
    except FileNotFoundError:
        pass

    return None


class ScreenshotOcrError(Exception):
    """A custom error for screenshot ocr."""


def log_exception(error: Exception) -> None:
    """Log an exception."""
    logger.exception(
        "Error: %s - %s",
        error.__class__.__name__,
        str(error),
    )
