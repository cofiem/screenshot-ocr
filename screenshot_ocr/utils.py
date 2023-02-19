import logging
import pathlib
import typing

logger = logging.getLogger(__name__)


def guess_path(
    path_prefix: pathlib.Path, path_suffix: str, name: str
) -> typing.Optional[pathlib.Path]:
    if not path_prefix:
        logger.debug(f"Base path for {name} was not provided.")
        return None

    expected_path = path_prefix / path_suffix if path_suffix else path_prefix
    if not expected_path.exists():
        logger.debug(f"Path for {name} does not exist.")
        return None

    logger.debug(f"Found the path for {name}: '{expected_path}'.")
    return expected_path
