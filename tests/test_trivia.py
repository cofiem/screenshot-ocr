import pytest

from screenshot_ocr.trivia import TriviaHelper


@pytest.mark.parametrize(
    ("line_text", "expected"),
    [
        ("QUESTION I\nbody text", (1, "body text")),
        ("Jeaffeal] QUESTION 22", (22, "")),
        ("QUESTION 4\n   body text   ", (4, "body text")),
        ("QUESTION 3o\n\n   body text   ", (30, "body text")),
        ("QUESTION li\n\n   body text \n  ", (11, "body text")),
    ],
)
def test_trivia_get_number_and_question(
    line_text,
    expected,
):
    helper = TriviaHelper(None, None)
    assert helper.get_number_and_question(line_text) == expected
