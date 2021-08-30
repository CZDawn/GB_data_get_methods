import json
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_db']
collection = db.hh_vacansies

with open('vacansies_info.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)
    print(data)

