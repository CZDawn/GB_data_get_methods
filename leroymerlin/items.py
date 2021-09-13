# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_price(value):
    value = value.replace('\xa0', '')
    value = ''.join(value.split(' '))
    try:
        return int(value)
    except:
        return value

def process_desc(value):
    value =  value.replace('\n                ', '')
    value = value.replace('\n            ', '')
    return value


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(process_desc))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()

