import re
import requests
import time

from bs4 import BeautifulSoup

from worker import classify

headers = {
    "Accept-Encoding": "gzip, deflate",
    'From': 'thisisjimah@gmail.com',
    'User-Agent': 'Firefly API Scraper'
}

base_url = "http://firefly.wikia.com"


def queue_url(url):
    """

    Stores the url in crawled urls.

    """
    pass


def valid_href(href):
    """

    Validates the given url to see if it should be added

    """
    if href is None:
        return False

    if "Special:" in href:
        return False

    if not re.match("^\/wiki\/[a-zA-Z&\/?]+", href):
        return False

    return True


def fire_at(url):
    """

    Hits the given url, queues urls found in the soup, extracts data.

    """
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')

        # Send our soup off for classification
        classify(soup)

        # Iterate through all available links and queue them if valid
        for link in soup.find_all('a'):
            l = link.get('href')

            if valid_href(l):
                queue_url(l)


def fire():
    links = []
    r = requests.get(
        "http://firefly.wikia.com/wiki/Main_Page",
        headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        classify(soup)

        for link in soup.findAll('a'):
            l = link.get('href')

            if valid_href(l):
                links.append(l)

    for i in range(2):
        print("Going to: " + links[i])
        r = requests.get(base_url + links[i])

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            for link in soup.findAll('a'):
                l = link.get('href')

                if valid_href(l):
                    links.append(l)

        print(links)
        time.sleep(10)


fire()
