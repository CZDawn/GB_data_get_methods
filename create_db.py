import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
collection = db.news


# Добавляет данные в базу из файла json
def pushDataToDatabase(data: list):
    for el in data:
        for item in el:
            collection.update_one(
                    {'name': item['name']},
                    {'$set': item}, upsert=True)

def fillDatabaseByData():
    with open('news.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        pushDataToDatabase(data)
    print('Done! Database is filled by data from json file.')

