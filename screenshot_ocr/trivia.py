import re


def extract_question_number_text(value: str):
    key_question = "question"
    number = None
    text = ""
    for line in value.splitlines():
        line_lower = line.casefold()

        if line.strip() and number is None and key_question in line_lower:
            number = int(line_lower.replace(key_question, "").strip())
            continue

        if not line.strip():
            continue
        text += " " + line.strip()

    text = text.strip()
    return number, text
