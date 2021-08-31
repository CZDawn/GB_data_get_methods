from lxml import html

def getNewsFromWebsite(newsObjects, xpathes, website):
    newsList = []
    for el in newsObjects:
        name = el.xpath(xpathes['name'])
        link = el.xpath(xpathes['link'])
        if xpathes['source'] == 'lenta.ru':
            source = ['lenta.ru']
        else:
            source = el.xpath(xpathes['source'])
        date_time = el.xpath(xpathes['dateTime'])
        newsData = {
            'name': name[0],
            'link': link[0],
            'source': source[0],
            'date_time': date_time[0],
            'website': website
        }
        newsList.append(newsData)
    return newsList


def getNewsFromYandex(dom, website):
    newsObjects = dom.xpath("//article[contains(@class, 'mg-card')]")
    xpathes = {
        'name': ".//h2[@class='mg-card__title']/text()",
        'link': ".//h2[@class='mg-card__title']/../@href",
        'source': ".//a[@class='mg-card__source-link']/text()",
        'dateTime': ".//span[@class='mg-card-source__time']/text()"
    }
    return getNewsFromWebsite(newsObjects, xpathes, website)


def getNewsFromLenta(dom, website):
    newsObjects = dom.xpath("//section[contains(@class, 'b-top7-for-main')]//div[@class='item']")
    xpathes = {
        'name': ".//a/text()",
        'link': ".//time[@class='g-time']/../@href",
        'source': 'lenta.ru',
        'dateTime': ".//time[@class='g-time']/@datetime"
    }
    return getNewsFromWebsite(newsObjects, xpathes, website)

