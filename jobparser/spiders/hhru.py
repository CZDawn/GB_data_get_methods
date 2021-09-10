import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://nn.hh.ru/search/vacancy?fromSearchLine='\
        'true&st=searchVacancy&text=python&area=1',
        'https://nn.hh.ru/search/vacancy?fromSearchLine='\
        'true&st=searchVacancy&text=python&area=2'
    ]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='vacansy-serp__vacansy-title']/@href").getall()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_vacansy)

    def parse_vacansy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary = response.xpath("//p[@class='vacansy-salary']/span/text()").get()
        vac_url = response.url
        yield JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)

