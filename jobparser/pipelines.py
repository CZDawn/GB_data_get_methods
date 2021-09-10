# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacansy0209

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_hh(item['salary'])
        elif spider.name == 'sjru':
            item['min_salary']. item['max_salary'], item['currency'] = self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        min_salary = self.get_min_salary_hh(salary)
        max_salary = self.get_max_salary_hh(salary)
        currency = self.get_salary_currency_hh(salary)
        return min_salary, max_salary, currency

    def process_salary_sj(self, salary):
        if 'от' in salary:
            vac_salary = salary[-1].replace(u'\xa0', u' ').split()
            min_salary = vac_salary[0] + vac_salary[1]
            max_salary = None
            currency = vac_salary[2]
            return int(min_salary), max_salary, currency
        if 'до' in salary:
            vac_salary = salary[-1].replace(u'\xa0', u' ').split()
            min_salary = None
            max_salary = vac_salary[0] + vac_salary[1]
            currency = vac_salary[2]
            return min_salary, int(max_salary), currency
        if salary[0] == 'По':
            min_salary = None
            max_salary = None
            currency = None
            return min_salary, max_salary, currency
        min_salary = salary[0].replace(u'\xa0', u'')
        max_salary = salary[1].replace(u'\xa0', u'')
        currency = salary[3]
        return int(min_salary), int(max_salary), currency

    def get_min_salary_hh(self, salary):
        result_list = []
        for el in salary.split():
            if el.isdigit():
                result_list.append(el)
        if len(result_list) >= 2 and result_list[1] == '000':
            return int(result_list[0] + result_list[1])
        return int(result_list[0])

    def get_max_salary_hh(self, salary):
        result_list = []
        for el in salary.split():
            if el.isdigit():
                result_list.append(el)
        if len(result_list) == 1:
            return int(result_list[0])
        if len(result_list) == 2 and result_list[1] == '000':
            return int(result_list[0] + result_list[1])
        if len(result_list) == 2 and result_list[1] != '000':
            return int(result_list[1])
        if len(result_list) == 3:
            return int(result_list[1] + result_list[2])
        return int(result_list[2] + result_list[3])

    def get_salary_currency_hh(self, salary):
        result_list = []
        for el in salary.split():
            if el.isdigit() == False:
                result_list.append(el)
        if 'бел.' in result_list:
            return result_list[-2] + result_list[-1]
        return result_list[-1]

