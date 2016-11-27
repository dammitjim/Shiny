import scrapy

from shiny.util.elements import clean_text_elements


class ShinySpider(scrapy.Spider):
    name = "shiny"
    start_urls = [
        "http://firefly.wikia.com/wiki/Malcolm_Reynolds",
        "http://firefly.wikia.com/wiki/Jayne_Cobb",
        "http://firefly.wikia.com/wiki/Kaywinnet_Lee_Frye",
    ]

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

            key = clean_text_elements(key_selector)
            if key is None:
                # TODO handle
                print("key fail")
                continue

            value = clean_text_elements(value_selector)
            if value is None:
                # TODO handle
                print("value fail")
                continue

            attributes[key] = value
        yield attributes
