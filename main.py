import json
import requests
from lxml import html
from create_db import fillDatabaseByData
from getNews import getNewsFromLenta, getNewsFromYandex

def getDocumentObject(link: str, userAgent: str):
    headers = {'User-Agent': userAgent}
    response = requests.get(link, headers=headers)
    return html.fromstring(response.text)


def createNewsDatabase(links: list, userAgent: str):
    result = []
    for link in links:
        dom = getDocumentObject(link, userAgent)
        if 'yandex.ru' in link.split('/'):
            result.append(getNewsFromYandex(dom, link))
        if 'lenta.ru' in link.split('/'):
            result.append(getNewsFromLenta(dom, link))
    with open('news.json', 'a', encoding='UTF-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    links = ['https://yandex.ru/news/', 'https://lenta.ru/']
    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '\
                'AppleWebKit/537.36 (KHTML, like Gecko) '\
                'Chrome/92.0.4515.159 Safari/537.36'
    createNewsDatabase(links, userAgent)
    fillDatabaseByData()

