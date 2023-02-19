import argparse
import logging
import pathlib
import shutil
import sys
import typing

from screenshot_ocr import tesseract, files

logger = logging.getLogger(__name__)


def build_args(args: list[str] = None) -> argparse.Namespace:
    # prog is set for pyOxidizer, due to issue: https://github.com/indygreg/PyOxidizer/issues/307
    parser = argparse.ArgumentParser(
        description="Extract text from screenshots.", prog="screenshot-ocr"
    )
    parser.add_argument(
        "--tesseract-exe",
        type=pathlib.Path,
        help="path to the Tesseract executable file",
    )
    parser.add_argument(
        "--tesseract-data",
        type=pathlib.Path,
        help="path to the Tesseract data directory",
    )
    parser.add_argument(
        "--input-dir",
        type=pathlib.Path,
        help="path to the folder containing the input images",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="path to the folder that will contain processed images",
    )
    parser.add_argument(
        "--no-move-images",
        action="store_true",
        help="don't move image files to the output directory (image files are moved by default)",
    )
    result = parser.parse_args(args)
    return result


def norm_args(args: list[str] = None):
    parsed_args = build_args(args)

    tesseract_install_dir_reg = tesseract.get_tesseract_install_dir_win_reg()
    tesseract_install_dir_guess = tesseract.get_tesseract_install_dir_win_guess()

    downloads_dir_reg = files.get_user_downloads_dir_win_guess()
    downloads_dir_guess = files.get_user_downloads_dir_win_reg()

    documents_dir_guess = files.get_user_documents_dir_win_guess()

    # Tesseract exe
    tesseract_exe = parsed_args.tesseract_exe
    if not tesseract_exe:
        tesseract_exe = tesseract.get_tesseract_executable_win_guess(
            tesseract_install_dir_reg
        )
        if not tesseract_exe:
            tesseract_exe = tesseract.get_tesseract_executable_win_guess(
                tesseract_install_dir_guess
            )

    # Tesseract tessdata
    tesseract_data = parsed_args.tesseract_data
    if not tesseract_data:
        tesseract_data = tesseract.get_tesseract_data_dir_win_guess(
            tesseract_install_dir_reg
        )
        if not tesseract_data:
            tesseract_data = tesseract.get_tesseract_data_dir_win_guess(
                tesseract_install_dir_guess
            )

    # input dir
    input_dir = parsed_args.input_dir
    if not input_dir:
        input_dir = downloads_dir_reg
        if not input_dir:
            input_dir = downloads_dir_guess

    # output dir
    output_dir = parsed_args.output_dir
    if not output_dir:
        output_dir = documents_dir_guess / "Tesseract"

    logger.info(f"Using Tesseract executable: '{tesseract_exe}'.")
    logger.info(f"Using Tesseract data: '{tesseract_data}'.")
    logger.info(f"Using input directory: '{input_dir}'.")
    logger.info(f"Using output directory: '{output_dir}'.")

    return {
        "tesseract_exe": tesseract_exe,
        "tesseract_data": tesseract_data,
        "input_dir": input_dir,
        "output_dir": output_dir,
        "no_move_images": parsed_args.no_move_images,
    }


def get_image_text(
    exe_path: pathlib.Path,
    data_dir: pathlib.Path,
    image_dir: pathlib.Path,
) -> typing.Tuple[pathlib.Path, str]:
    for image_file in files.find_ff_screenshot_files(image_dir):
        output_text = tesseract.run_tesseract(exe_path, data_dir, image_file)
        yield image_file, output_text


def run_program(args: list[str] = None) -> None:
    logger.info("Starting Screenshot OCR...")

    # get the arguments
    normalised_arguments = norm_args(args)
    tesseract_exe = normalised_arguments["tesseract_exe"]
    tesseract_data = normalised_arguments["tesseract_data"]
    input_dir = normalised_arguments["input_dir"]
    output_dir = normalised_arguments["output_dir"]
    move_images = not normalised_arguments["no_move_images"]

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    count = 0

    # find the image files and extract the text from each
    for image_file, output_text in get_image_text(
        tesseract_exe, tesseract_data, input_dir
    ):
        if move_images:
            # move the image file to the output dir
            shutil.move(image_file, output_dir / image_file.name)

        # create a text file with the same name as the image file that contains the extracted text
        (output_dir / image_file.stem).with_suffix(".txt").write_text(output_text)

        # print the image file name and extracted text to stdout
        logger.info(f"{image_file.name}: {output_text}")

        count += 1

    logger.info(f"Found and processed {count} image file(s).")
    logger.info("...finished.")
