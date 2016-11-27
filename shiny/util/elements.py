import re

_reference_regex = re.compile('\[[0-9]*\]')


def _should_ignore_text_element(text_element):
    """Check if the provided element should be skipped."""
    text_element = text_element.strip()
    if text_element == "":
        return True

    if text_element == ",":
        return True

    if text_element.startswith("\\"):
        return True

    if _reference_regex.match(text_element):
        return True

    return False


def _sketchy_string_replacements(text):
    """Run any sketchy string replaces here."""
    _text = text
    _text.replace(u'\xa0', u' ')
    return _text


def clean_text_element(text_element):
    """Clean an individual text string.

    :type text_element: string
    """
    text_element = text_element.strip()

    if text_element.startswith(','):
        text_element = text_element[1:]

    if text_element.endswith(','):
        text_element = text_element[:len(text_element) - 1]

    text_element = _sketchy_string_replacements(text_element)

    return text_element


def clean_text_elements(text_elements):
    """Clean the list of text elements extracted from a selector.

    :param text_elements: the extracted raw strings
    :return: a clean usable string
    """
    cleaned = []

    for element in text_elements:
        if _should_ignore_text_element(element):
            continue

        cleaned.append(clean_text_element(element))

    return "||".join(cleaned)
