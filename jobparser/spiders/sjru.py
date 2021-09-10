import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://spb.superjob.ru/vacancy/search/?keywords=python',
        'https://www.superjob.ru/vacancy/search/?keywords=python&'\
        'geo%5Bt%5D%5B0%5D=4'
    ]

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//div[@class='f-test-search-result-item']"\
            "//a[contains(@class, '_6AfZ9')]/@href").getall()

        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href")
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_vacansy)

    def parse_vacansy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//span[contains(@class, 'ZON4b')]//span[contains(@class, '_2Wp8I')]/text()").get()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)

