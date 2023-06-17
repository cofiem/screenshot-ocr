import re

import pytest

pytest.register_assert_rewrite("helpers")


@pytest.fixture()
def equal_ignore_whitespace():
    def _equal_ignore_whitespace(value1: str, value2: str, ignore_case=False):
        # Ignore non-space and non-word characters
        whitespace = re.compile(r"\s+")
        replace1 = whitespace.sub(" ", value1 or "").strip()
        replace2 = whitespace.sub(" ", value2 or "").strip()

        if ignore_case:
            assert replace1.casefold() == replace2.casefold()
        else:
            assert replace1 == replace2

    return _equal_ignore_whitespace


@pytest.fixture()
def collapse_whitespace():
    def _collapse_whitespace(value: str):
        # Ignore non-space and non-word characters
        whitespace = re.compile(r"\s+")
        replace = whitespace.sub(" ", value or "").strip()
        return replace

    return _collapse_whitespace
