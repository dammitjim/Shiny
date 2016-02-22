import re
import requests
import time

from bs4 import BeautifulSoup

headers = {
    "Accept-Encoding": "gzip, deflate",
    'From': 'thisisjimah@gmail.com',
    'User-Agent': 'Firefly API Scraper'
}

base_url = "http://firefly.wikia.com"


def valid_href(href):
    if href is None:
        return False
    if "Special:" in href:
        return False
    if not re.match("^\/wiki\/[a-zA-Z&\/?]+", href):
        return False
    return True


def classify(soup):
    pass


def classify_character(soup):
    pass


def classify_episode(soup):
    pass


def classify_actor(soup):
    pass


def fire():
    links = []
    r = requests.get(
        "http://firefly.wikia.com/wiki/Main_Page",
        headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text)

        for link in soup.findAll('a'):
            l = link.get('href')
            if valid_href(l):
                links.append(l)

    for i in range(2):
        print("Going to: " + links[i])
        r = requests.get(base_url + links[i])
        if r.status_code == 200:
            soup = BeautifulSoup(r.text)
            for link in soup.findAll('a'):
                l = link.get('href')
                if valid_href(l):
                    links.append(l)
        print(links)
        time.sleep(10)


fire()
