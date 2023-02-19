import logging
import pathlib
import subprocess
import sys
import typing

from screenshot_ocr import utils

logger = logging.getLogger(__name__)


def get_tesseract_install_dir_win_guess() -> typing.Optional[pathlib.Path]:
    if sys.platform != "win32":
        logger.debug("Cannot use Windows default path on non-Windows platform.")
        return None

    import os

    env_var = os.environ.get("PROGRAMFILES")
    if not env_var or not env_var.strip():
        env_var = "C:\\Program Files"

    return utils.guess_path(pathlib.Path(env_var), "Tesseract-OCR", "Tesseract")


def get_tesseract_install_dir_win_reg() -> typing.Optional[pathlib.Path]:
    if sys.platform != "win32":
        logger.debug("Cannot use Windows registry on non-Windows platform.")
        return None

    import winreg

    tree_root = winreg.HKEY_LOCAL_MACHINE
    tree_leaf = winreg.OpenKeyEx(tree_root, r"SOFTWARE\\Tesseract-OCR\\")
    key_value, key_type = winreg.QueryValueEx(tree_leaf, "InstallDir")
    if tree_leaf:
        winreg.CloseKey(tree_leaf)

    if key_value and key_type == winreg.REG_SZ:
        logger.debug(
            f"Found Tesseract install directory from Windows registry: '{key_value}'."
        )
        return pathlib.Path(key_value)

    logger.debug("Could not find Tesseract install directory in Windows registry.")
    return None


def get_tesseract_data_dir_win_guess(
    install_dir: pathlib.Path,
) -> typing.Optional[pathlib.Path]:
    return utils.guess_path(install_dir, "tessdata", "Tesseract data")


def get_tesseract_executable_win_guess(
    install_dir: pathlib.Path,
) -> typing.Optional[pathlib.Path]:
    return utils.guess_path(install_dir, "tesseract.exe", "Tesseract program")


def run_tesseract(
    exe_path: pathlib.Path,
    data_dir: pathlib.Path,
    image_file: pathlib.Path,
):
    cmds = [
        str(exe_path),
        "--tessdata-dir",
        str(data_dir),
        str(image_file),
        "stdout",
    ]
    result = subprocess.run(cmds, check=True, capture_output=True)
    return result.stdout.decode(encoding="UTF-8")
