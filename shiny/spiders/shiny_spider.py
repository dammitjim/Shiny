import re

import scrapy


class ShinySpider(scrapy.Spider):
    name = "shiny"
    start_urls = [
        "http://firefly.wikia.com/wiki/Malcolm_Reynolds",
    ]
    reference_regex = re.compile('\[[0-9]*\]')

    def _is_garbage(self, text_element):
        if text_element.startswith("\\"):
            return True

        if text_element == "":
            return True

        if text_element == ",":
            return True

        if self.reference_regex.match(text_element):
            return True

        return False

    @staticmethod
    def _clean_text(text_element):
        if text_element.startswith(","):
            text_element = text_element[1:]

        if text_element.endswith(","):
            text_element = text_element[:len(text_element) - 1]

        return text_element.strip()

    def _extract_selector_text(self, elements):
        els = []

        for element in elements:
            el = element.strip()

            if self._is_garbage(el):
                continue

            els.append(self._clean_text(el))

        return ",".join(els)

    def parse(self, response):
        attributes = {}

        title_element = response.css(".header-title h1::text").extract()

        if len(title_element) == 0:
            return

        attributes["title"] = title_element[0]

        infobox = response.css("table.infoboxtable")
        for row in infobox.css("tr"):
            data_nodes = row.css("td")

            if len(data_nodes) < 2:
                continue

            key_selector = data_nodes[0].css("::text").extract()
            value_selector = data_nodes[1].css("::text").extract()

            key = self._extract_selector_text(key_selector)
            if key is None:
                # TODO handle
                print("key fail")
                continue

            value = self._extract_selector_text(value_selector)
            if value is None:
                # TODO handle
                print("value fail")
                continue

            attributes[key] = value
        yield attributes
