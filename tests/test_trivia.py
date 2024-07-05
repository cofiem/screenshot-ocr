import pytest

from screenshot_ocr.trivia import TriviaHelper

example_1_longer_question = "QUESTION 15"
example_1_longer_text = """
Last month we did a Family Feud-style survey on the Isolation
Trivia Facebook page.
For three points — what were the top three responses to this
question:
THREE POINTS
"""
example_1_longer_all = f"""{example_1_longer_question}
{example_1_longer_text}
"""


example_2_longer_question = "QUESTION 6"
example_2_longer_text = """
body text for q6

50. FOUR POINTS
"""
example_2_longer_all = f"""{example_2_longer_question}
{example_2_longer_text}
"""


example_3_longer_question = "QUESTION 27"
example_3_longer_text = """

body text
q3

SO. THREE POINTS

"""
example_3_longer_all = f"""{example_3_longer_question}
{example_3_longer_text}
"""


@pytest.mark.parametrize(
    ("line_text", "expected"),
    [
        ("QUESTION I\nbody text", (1, 1, "body text")),
        ("Jeaffeal] QUESTION 22", (22, 1, "")),
        ("QUESTION 4\n   body text   ", (4, 1, "body text")),
        ("QUESTION 3o\n\n   body text   ", (30, 1, "body text")),
        ("QUESTION li\n\n   body text \n  ", (11, 1, "body text")),
        (example_1_longer_all, (15, 3, example_1_longer_text)),
        (example_2_longer_all, (6, 4, example_2_longer_text)),
        (example_3_longer_all, (27, 3, example_3_longer_text)),
    ],
)
def test_trivia_get_number_and_question(
    line_text,
    expected,
):
    helper = TriviaHelper(None, None)
    actual_question, actual_points, actual_text = helper.get_text_details(line_text)
    expected_question, expected_points, expected_text = expected
    assert actual_question == expected_question
    assert actual_points == expected_points
    assert actual_text == expected_text.replace("\n\n", "\n").replace("\n", " ").strip()
