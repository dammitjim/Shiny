from bs4 import BeautifulSoup


def classify(soup):
    """

    Generic classification function, takes the soup of a page and
    extracts relevant information.

    Identifies the page type and routes through to the appropriate
    classification function.

    """
    assert isinstance(soup, BeautifulSoup)

    if is_character(soup):
        classify_character(soup)
        return

    if is_actor(soup):
        classify_actor(soup)
        return

    if is_episode(soup):
        classify_episode(soup)
        return


def classify_character(soup):
    """

    Extracts information from the soup relevant to the given character.

    """
    assert isinstance(soup, BeautifulSoup)
    pass


def classify_episode(soup):
    """

    Extracts information from the soup relevant to the given episode.

    """
    assert isinstance(soup, BeautifulSoup)
    pass


def classify_actor(soup):
    """

    Extracts information for the given actor.

    """
    assert isinstance(soup, BeautifulSoup)
    pass


def is_character(soup):
    """

    Returns whether the page is of type Character.

    """
    assert isinstance(soup, BeautifulSoup)
    return False


def is_episode(soup):
    """

    Returns whether the page is of type Episode.

    """
    assert isinstance(soup, BeautifulSoup)
    return False


def is_actor(soup):
    """

    Returns whether the page is of type Actor.

    """
    assert isinstance(soup, BeautifulSoup)
    return False
