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
python -m pip install --upgrade pip setuptools wheel
python -m pip install --upgrade -r requirements-dev.txt -r requirements.txt

# check for outdated packages
pip list --outdated
```

## Run tests and linters

Run the tests and linters with multiple python versions using tox.

If the pip dependencies have changed, it might be necessary to 
(un)comment `recreate = true` in the tox section in `pyproject.toml`.

To run using all available python versions:

```bash
python -X dev -m tox
```

To run using the active python:

```bash
python -X dev -m tox -e py
```

## Generate docs

Generate the docs:

```bash
pdoc --docformat google \
  --edit-url screenshot_ocr=https://github.com/cofiem/screenshot-ocr/blob/main/src/screenshot_ocr/ \
  --search --show-source \
  --output-directory docs \
  ./src/screenshot_ocr
```

## Create and upload release

Generate the distribution package archives.

```bash
python -X dev -m build
```

Upload archives to Test PyPI first.

```bash
python -X dev -m twine upload --repository testpypi dist/*
```

When uploading:

- for username, use `__token__`
- for password, [create a token](https://test.pypi.org/manage/account/#api-tokens)

Go to the [test project page](https://test.pypi.org/project/screenshot-ocr) and check that it looks ok.

Then create a new virtual environment, install the dependencies, and install from Test PyPI.

```bash
rm -rf .venv-test
python -m venv .venv-test
source .venv-test/bin/activate
python -m pip install --upgrade pip setuptools wheel

# use the requirements file to install dependencies from the production PyPI,
# as the packages may not be on Test PyPI, or they might be different packages.
python -m pip install --upgrade -r requirements.txt

TESTING_PY_VERSION='0.0.1'
pip install --index-url https://test.pypi.org/simple/ --no-deps screenshot-ocr==$TESTING_PY_VERSION
# or
pip install dist/screenshot_ocr-$TESTING_PY_VERSION-py3-none-any.whl
```

Test the installed package.

```bash
screenshot-ocr --version
screenshot-ocr --help
screenshot-ocr tests/resources/examples/Screenshot 2023-06-09 at 18-45-03 Example.png
```

If the package seems to work as expected, upload it to the live PyPI.

```bash
python -X dev -m twine upload dist/*
```

When uploading:

- for username, use `__token__`
- for password, [create a token](https://pypi.org/manage/account/#api-tokens)

Go to the [live project page](https://pypi.org/project/screenshot-ocr) and check that it looks ok.

Done!
