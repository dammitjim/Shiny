import re
from typing import List

_reference_regex = re.compile('\[[0-9]*\]')


def _should_ignore_text_element(text_element: str) -> bool:
    """Check if the provided element should be skipped."""
    if text_element == "":
        return True

    if text_element == ",":
        return True

    if text_element.startswith("\\"):
        return True

    if _reference_regex.match(text_element):
        return True

    return False


def clean_text_element(text_element: str):
    """Clean an individual text string.

    :type text_element: string
    """
    if text_element.startswith(','):
        text_element = text_element[1:]

    if text_element.endswith(','):
        text_element = text_element[:len(text_element) - 1]

    return text_element.strip()


def clean_text_elements(text_elements: List[str]) -> str:
    """Clean the list of text elements extracted from a selector.

    :param text_elements: the extracted raw strings
    :return: a clean usable string
    """
    cleaned = []

    for element in text_elements:
        if _should_ignore_text_element(element):
            continue

        cleaned.append(clean_text_element(element))

    return ",".join(cleaned)
