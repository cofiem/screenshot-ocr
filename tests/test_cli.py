from click.testing import CliRunner
from screenshot_ocr.cli import screenshot_ocr


def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(screenshot_ocr, [])
    assert "Error: Missing argument 'SPREADSHEET_ID'" in result.output
    expected_code = 2
    assert result.exit_code == expected_code


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(screenshot_ocr, ["--help"])
    assert "Usage: screenshot-ocr" in result.output
    assert result.exit_code == 0


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(screenshot_ocr, ["--version"])
    assert "Screenshot OCR, version" in result.output
    assert result.exit_code == 0
