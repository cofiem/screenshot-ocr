# Screenshot OCR contributing guide

## Development

Create a virtual environment:

```bash
python -m venv .venv
```

Install runtime dependencies and development dependencies:

```bash
# Windows
.venv\Scripts\activate.ps1

# Linux
source .venv/bin/activate

# install dependencies
python -m pip install --upgrade pip tox build
```

## Run tests and linters

Run the tests and linters with multiple python versions using tox.

To run using all available python versions:

```bash
python -X dev -m tox run -e ALL
```

To run using the active python:

```bash
python -X dev -m tox -e py
```

## Test a release locally

Generate the distribution package archives.

```bash
python -X dev -m build
```

Then create a new virtual environment, install the dependencies, and install from the local wheelTest PyPI.

```bash
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate

python -m pip install --upgrade pip

pip install dist/screenshot_ocr-$SCREENSHOT_OCR_VERSION-py3-none-any.whl
```

Test the installed package.

```bash
screenshot-ocr --version
screenshot-ocr --help

SCREENSHOT_OCR_TEST_DIR="$PWD/tests/resources/examples"
screenshot-ocr no-spreadsshet-id --no-move-images --log-level debug \
  --input-dir "$SCREENSHOT_OCR_TEST_DIR" \
  --output-dir "$SCREENSHOT_OCR_TEST_DIR" \
  --google-credentials "$SCREENSHOT_OCR_TEST_DIR/empty_credentials.json" \
  --google-token "$SCREENSHOT_OCR_TEST_DIR/token.json"
```

Example of the output that is expected:

```text
2023-06-18 14:47:23,385 [DEBUG   ] Found tesseract executable using Windows install information at 'C:\Program Files\Tesseract-OCR\tesseract.exe'.
2023-06-18 14:47:23,386 [DEBUG   ] Found tesseract data using Windows install information at 'C:\Program Files\Tesseract-OCR\tessdata'.
2023-06-18 14:47:23,386 [INFO    ] Using input directory: '<base-path>\screenshot-ocr\tests\resources\examples'.
2023-06-18 14:47:23,386 [INFO    ] Using output directory: '<base-path>\screenshot-ocr\tests\resources\examples'.
2023-06-18 14:47:23,386 [INFO    ] Using Tesseract executable: 'C:\Program Files\Tesseract-OCR\tesseract.exe'.
2023-06-18 14:47:23,386 [INFO    ] Using Tesseract data: 'C:\Program Files\Tesseract-OCR\tessdata'.
2023-06-18 14:47:23,386 [INFO    ] Using Google credentials: '<base-path>\screenshot-ocr\tests\resources\examples\empty_credentials.json'.
2023-06-18 14:47:23,386 [INFO    ] Using Google token: '<base-path>\screenshot-ocr\tests\resources\examples\token.json'.
2023-06-18 14:47:23,386 [INFO    ] Starting Screenshot OCR.
2023-06-18 14:47:23,386 [INFO    ] Looking for screenshot images in '<base-path>\screenshot-ocr\tests\resources\examples'.
2023-06-18 14:47:23,550 [INFO    ] "Screenshot 2023-06-16 at 18-49-13 Facebook.png": Q17) "Which bird lays the largest eggs? (In terms of the size of a single egg)"
2023-06-18 14:47:23,550 [INFO    ] Starting authorisation flow.
2023-06-18 14:47:23,551 [ERROR   ] Error: ValueError - Client secrets must be for a web or installed app.
Traceback (most recent call last):
[..snip..]
ValueError: Client secrets must be for a web or installed app.
```

## Test a release from Test PyPI

If the package seems to work as expected, push changes to the `main` branch.

Push changes to the `main` branch.
The `pypi-package.yml` GitHub Actions workflow will deploy a release to Test PyPI.

Then follow the same process as testing a release locally, except install from Test PyPI.

```bash
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate

python -m pip install --upgrade pip

# use the requirements file to install dependencies from the production PyPI,
# as the packages may not be on Test PyPI, or they might be different (potentially malicious!) packages.
python -m pip install --upgrade -r requirements.txt

pip install --index-url https://test.pypi.org/simple/ --no-deps screenshot-ocr==$SCREENSHOT_OCR_VERSION
```

## Create a release to PyPI

Create a tag on the `main` branch.
The `pypi-package.yml` GitHub Actions workflow will deploy a release to PyPI.

Go to the [live project page](https://pypi.org/project/screenshot-ocr) and check that it looks ok.

Done!
