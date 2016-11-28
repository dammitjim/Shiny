import scrapy

from scrapy.utils.response import get_base_url

from shiny.util.elements import clean_text_elements

CLASSIFICATION_PERSON = "Person"


class ShinySpider(scrapy.Spider):
    name = "shiny"
    base_url = "http://firefly.wikia.com"
    start_urls = [
        "http://firefly.wikia.com/wiki/Malcolm_Reynolds",
    ]

    def _get_classification(self, parsed_elements):
        """Determine if this page should be parsed or skipped.

        Based on the infobox DOM element.

        """
        for key in parsed_elements.keys():
            if key == "Gender":
                return CLASSIFICATION_PERSON

        return None

    def parse(self, response):
        attributes = {}

        title_element = response.css(".header-title h1::text").extract()

        if len(title_element) == 0:
            return

        attributes["title"] = title_element[0]

        infobox = response.css("table.infoboxtable")
        if len(infobox) == 0:
            self.logger.error("no infobox present for page")
            return

        for row in infobox.css("tr"):
            data_nodes = row.css("td")

            if len(data_nodes) < 2:
                continue

            key_selector = data_nodes[0].css("::text").extract()
            value_selector = data_nodes[1].css("::text").extract()

            key = clean_text_elements(key_selector)
            if key is None:
                self.logger.error("unable to clean key " + key_selector)
                continue

            value = clean_text_elements(value_selector)
            if value is None:
                self.logger.error("unable to clean value " + value_selector)
                continue

            attributes[key] = value

        for href in response.css("#WikiaArticle a::attr(href)"):
            extr = href.extract()
            if not extr.startswith("/"):
                self.logger.warn("not following url: " + extr)
                continue
            if "?" in extr:
                spl = extr.split("?")
                extr = spl[0]
            yield scrapy.Request(
                self.base_url + extr, callback=self.parse)

        clfc = self._get_classification(attributes)
        if clfc is None:
            self.logger.error("unable to determine classification page: {0}"
                              .format(attributes))
            return

        url = get_base_url(response)
        attributes["WIKI_URL"] = url

        yield attributes
