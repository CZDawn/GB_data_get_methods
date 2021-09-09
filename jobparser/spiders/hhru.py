import scrapy
from scrapy.http import HtmlResponse


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://nn.hh.ru/search/vacancy?fromSearchLine='\
        'true&st=searchVacancy&text=python&area=1',
        'https://nn.hh.ru/search/vacancy?fromSearchLine='\
        'true&st=searchVacancy&text=python&area=2']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='vacansy-serp__vacansy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_vacansy)

    def parse_vacansy(self, response: HtmlResponse):
        print()

