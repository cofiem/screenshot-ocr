import logging
import pathlib
import sys

from screenshot_ocr import utils

logger = logging.getLogger(__name__)


def get_user_downloads_dir_win_guess():
    if sys.platform != "win32":
        logger.debug("Cannot use Windows default path on non-Windows platform.")
        return None

    import os

    env_var = os.environ.get("USERPROFILE")
    if not env_var or not env_var.strip():
        logger.debug("The Windows current user profile path %USERPROFILE% is not set.")
        return None

    return utils.guess_path(pathlib.Path(env_var), "Downloads", "user downloads")


def get_user_downloads_dir_win_reg():
    if sys.platform != "win32":
        logger.debug("Cannot use Windows registry on non-Windows platform.")
        return None

    import winreg

    tree_root = winreg.HKEY_CURRENT_USER
    tree_leaf = winreg.OpenKeyEx(
        tree_root,
        r"SOFTWARE\\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders\\",
    )
    key_value, key_type = winreg.QueryValueEx(
        tree_leaf, "{374DE290-123F-4565-9164-39C4925E467B}"
    )
    if tree_leaf:
        winreg.CloseKey(tree_leaf)

    if key_value and key_type == winreg.REG_SZ:
        logger.debug(
            f"Found user downloads directory from Windows registry: '{key_value}'."
        )
        return pathlib.Path(key_value)

    logger.debug("Could not find user downloads directory in Windows registry.")
    return None


def get_user_documents_dir_win_guess():
    if sys.platform != "win32":
        logger.debug("Cannot use Windows default path on non-Windows platform.")
        return None

    import os

    env_var = os.environ.get("USERPROFILE")
    if not env_var or not env_var.strip():
        logger.debug("The Windows current user profile path %USERPROFILE% is not set.")
        return None

    return utils.guess_path(pathlib.Path(env_var), "Documents", "user documents")


def find_ff_screenshot_files(image_dir: pathlib.Path):
    """Yield the FireFox screenshot files."""
    logger.info(
        f"Looking for files in '{image_dir}' "
        "that match the pattern 'Screenshot [date] Facebook.png'."
    )
    for file_path in image_dir.iterdir():
        if not file_path.is_file():
            continue
        if file_path.suffix != ".png":
            continue
        if not file_path.stem.startswith("Screenshot "):
            continue
        if not file_path.stem.endswith("Facebook"):
            continue

        yield file_path
