import os
import pathlib
import sys

import pytest

from screenshot_ocr import utils
from screenshot_ocr.app_paths import DefaultPaths
from tests.helpers import normalise_path


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Windows-specific test.")
def test_app_paths_windows():
    d = DefaultPaths(allow_not_exist=True)
    app_name = utils.get_name_dash()
    author_name = utils.get_author_dash()

    user_profile = pathlib.Path.home()

    # user profile
    documents_dir = d.documents_dir
    downloads_dir = d.downloads_dir

    assert documents_dir == user_profile / "Documents"
    assert downloads_dir == user_profile / "Downloads"

    # user app config
    google_credentials_file = d.google_credentials_file
    google_token_file = d.google_token_file

    local_app_data_raw = os.environ.get("LOCALAPPDATA")
    local_app_data = (
        pathlib.Path(local_app_data_raw)
        if local_app_data_raw
        else user_profile / "AppData" / "Local"
    )
    base_config_dir = local_app_data / author_name / app_name

    assert normalise_path(google_credentials_file) == normalise_path(
        base_config_dir / "credentials.json",
    )
    assert normalise_path(google_token_file) == normalise_path(
        base_config_dir / "token.json",
    )

    # shared program install
    tesseract_exe_file = d.tesseract_exe_file
    tesseract_data_file = d.tesseract_data_file

    program_files_raw = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    program_files = pathlib.Path(program_files_raw)
    base_program_dir = program_files / "Tesseract-OCR"

    assert tesseract_exe_file == base_program_dir / "tesseract.exe"
    assert tesseract_data_file == base_program_dir / "tessdata"


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux-specific test.")
def test_app_paths_linux():
    d = DefaultPaths(allow_not_exist=True)
    app_name = utils.get_name_dash()
    utils.get_author_dash()

    user_profile = pathlib.Path.home()

    # user profile
    documents_dir = d.documents_dir
    downloads_dir = d.downloads_dir

    assert documents_dir == user_profile / "Documents"
    assert downloads_dir == user_profile / "Downloads"

    # user app config
    google_credentials_file = d.google_credentials_file
    google_token_file = d.google_token_file

    local_app_data = pathlib.Path("~/.config")
    base_config_dir = local_app_data / app_name

    assert normalise_path(google_credentials_file) == normalise_path(
        base_config_dir / "credentials.json",
    )
    assert normalise_path(google_token_file) == normalise_path(
        base_config_dir / "token.json",
    )

    # shared program install
    tesseract_exe_file = d.tesseract_exe_file
    tesseract_data_file = d.tesseract_data_file

    assert tesseract_exe_file == pathlib.Path("/usr/bin/tesseract")
    assert tesseract_data_file == pathlib.Path(
        "/usr/share/tesseract-ocr/4.00/tessdata/",
    )
