import scrapy
from scrapy.http import HtmlResponse
from items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/vhodnye-dveri/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[contains(@class, 'phytpj4_plp')]/a")
        for link in links:
            yield response.follow(link, callback=self.parse_links)

    def parse_links(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath(
            'description',
            "//dt[@class='def-list__term']/text() |"\
            "//dd[@class='def-list__definition']/text()"
        )
        loader.add_value('url', response.url)
        loader.add_xpath(
            'photos',
            "//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset"
        )
        yield loader.load_item()
