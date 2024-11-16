import re
import sys

import pytest

from screenshot_ocr import cli, utils


if sys.version_info >= (3, 10):
    help_phrase_options = "options:"
else:
    help_phrase_options = "optional arguments:"


def test_cli_help(capsys, caplog, equal_ignore_whitespace):
    with pytest.raises(SystemExit, match=str(0)):
        cli.main(["--help"])

    program_help = f"""usage: screenshot-ocr [-h] [--version] [--input-dir INPUT_DIR]
                      [--output-dir OUTPUT_DIR]
                      [--tesseract-exe TESSERACT_EXE]
                      [--tesseract-data TESSERACT_DATA] [--no-move-images]
                      [--google-credentials GOOGLE_CREDENTIALS]
                      [--google-token GOOGLE_TOKEN]
                      [--log-level {{debug,info,warning,error,critical}}]
                      spreadsheet_id

Extract text from screenshots.

positional arguments:
  spreadsheet_id        the Google Docs spreadsheet id

{help_phrase_options}
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --input-dir INPUT_DIR
                        path to the folder containing the input images
  --output-dir OUTPUT_DIR
                        path to the folder that will contain processed images
                        and text files
  --tesseract-exe TESSERACT_EXE
                        path to the Tesseract executable file
  --tesseract-data TESSERACT_DATA
                        path to the Tesseract data directory
  --no-move-images      don't move image files to the output directory (image
                        files are moved by default)
  --google-credentials GOOGLE_CREDENTIALS
                        path to the Google OAuth credentials / client secrets
                        json file
  --google-token GOOGLE_TOKEN
                        path to the file containing the current authorisation
                        token data
  --log-level {{debug,info,warning,error,critical}}
                        the log level: debug, info, warning, error, critical"""

    cap_stdout, cap_stderr = capsys.readouterr()
    assert cap_stderr == ""
    equal_ignore_whitespace(cap_stdout, program_help)
    assert caplog.record_tuples == []


def test_cli_no_args(capsys, caplog, equal_ignore_whitespace):
    with pytest.raises(SystemExit, match=str(2)):
        cli.main([])

    program_error = """usage: screenshot-ocr [-h] [--version] [--input-dir INPUT_DIR]
                      [--output-dir OUTPUT_DIR]
                      [--tesseract-exe TESSERACT_EXE]
                      [--tesseract-data TESSERACT_DATA] [--no-move-images]
                      [--google-credentials GOOGLE_CREDENTIALS]
                      [--google-token GOOGLE_TOKEN]
                      [--log-level {debug,info,warning,error,critical}]
                      spreadsheet_id
screenshot-ocr: error: the following arguments are required: spreadsheet_id"""

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    equal_ignore_whitespace(stderr, program_error)
    assert caplog.record_tuples == []


def test_cli_version(capsys, caplog):
    with pytest.raises(SystemExit, match="0"):
        cli.main(["--version"])

    stdout, stderr = capsys.readouterr()
    assert re.fullmatch(
        rf"{utils.get_name_dash()}\s+\d+\.\d+\.\d+(\.dev\d+)?\n$", stdout
    )
    assert stderr == ""
    assert caplog.record_tuples == []
