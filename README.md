# screenshot-ocr

Extract text from screenshots.

## Overview

This command line program will process images in a directory,
move processed images to another directory,
and enter the extracted text into cells in a Google Docs spreadsheet.

Initially created to extract text from screenshots of online trivia.
This made it easier to put the question into a spreadsheet,
so that people who were unable to watch the stream could participate.

If you're looking for a more generic program to extract structured text from pdfs and images,
try [leaf-focus](https://github.com/anotherbyte-net/leaf-focus).

## Install and Setup

There are three things to set up to get a working installation:
1. Python and this package
2. Tesseract for OCR
3. Access to the Google Docs spreadsheet

### Python and this package

[![PyPI - Version](https://img.shields.io/pypi/v/screenshot-ocr)](https://pypi.org/project/screenshot-ocr)


1. Have a look at the [RealPython guide to install Python](https://realpython.com/installing-python)
and check the version of Python that is installed.

2. Try using [pipx](https://pypa.github.io/pipx/installation/) to install `screenshot-ocr`.

3. Create and activate a Python virtual environment (`venv`).
The [Python Packaging Guide shows how to create a venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).

For example:

```bash
# create the venv
python -m venv screenshot-ocr-venv

# activate the venv
source screenshot-ocr-venv/bin/activate

# update the package installation tools
python -m pip install --upgrade pip setuptools wheel
```

4. Install this package (`screenshot-ocr`) from PyPI using pip.

For example:

```bash
# install this package
pip install screenshot-ocr
```

5. Show the `screenshot-ocr` help and version to check it is installed.

For example:

```bash
# show the command line help
screenshot-ocr --help

# or, without the venv activated
screenshot-ocr-venv/bin/screenshot-ocr --help
screenshot-ocr-venv/Scripts/screenshot-ocr --help

# show the version
screenshot-ocr --version
```

### Tesseract for OCR

Tesseract OCR is used for Optical Character Recognition.

It must be installed separately. [Install tesseract](https://tesseract-ocr.github.io/tessdoc/#binaries).

On Debian and Ubuntu and similar Linux distributions, there might be an apt package available.

For example:

```bash
sudo apt install tesseract-ocr
```

### Access to the Google Docs spreadsheet

This app uses the Google OAuth Installed App Flow to gain access to the spreadsheet.

[Follow the guide to set up your access](https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth.md#acquiring-client-ids-and-secrets). 

You'll need to provide a `credentials.json` (`client_secrets.json`) file.

You can download this from the Google Cloud -> APIs and Services -> Credentials page.

Under "OAuth 2.0 Client IDs",
for a "Desktop" type client,
use the "Download OAuth client" action,
then "Download JSON" to get a `credentials.json`

If there is no valid token,
you'll be prompted to log in with your Google account through your browser,
and asked to authorise the app's access to Google Docs spreadsheets.

If this process succeeds,
this program will create a token file that will be used for subsequent access.

## Usage

All optional arguments have reasonable defaults. Try using the defaults first.

If you run into issues, you can also specify the paths to the required files.

```bash
# use all the defaults: ocr tool and data files,
# input dir, output dir, credentials and token files
screenshot-ocr "<google-docs-spreadsheet-id>"

# use the defaults, except for the ocr binary and data file paths
screenshot-ocr "<google-docs-spreadsheet-id>" \
  --tesseract-exe "<path-to-file>" \
  --tesseract-data "<path-to-dir>"

# specify everything: ocr binary and data files,
# input dir, output dir, credentials and token files
screenshot-ocr "<google-docs-spreadsheet-id>" \
  --input-dir "<path-to-dir>" \
  --output-dir "<path-to-dir>" \
  --tesseract-exe "<path-to-file>" \
  --tesseract-data "<path-to-dir>" \
  --google-credentials "<path-to-file>" \
  --google-token "<path-to-file>"
```
