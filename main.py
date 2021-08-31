import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_db']
collection = db.hh_vacansies


# Добавляет данные в базу из файла json
def pushDataToDataBase(data: list):
    for el in data:
        for item in el:
            collection.update_one(
                    {'vacansy_link': item['vacansy_link']},
                    {'$set': item}, upsert=True)

def fillDataBaseByData():
    with open('vacansies_info.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        pushDataToDataBase(data)
    print('Done! Data Base is filled by data from json file.')

fillDataBaseByData()


# Ищет все записи в базе у которых зарплата от 120000 до 200000
def findVacansiesByCondition():
    for el in collection.find({'$and': [
                              {'salary_info.min_salary': {'$gt': 120000}},
                              {'salary_info.max_salary': {'$lt': 200000}},
                              {'salary_info.salary_currency': 'руб.'}]}):
        pprint(el)

findVacansiesByCondition()

