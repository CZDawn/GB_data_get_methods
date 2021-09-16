# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:
    def process_item(self, item, spider):
        desc_list = item['description']
        desc_data = []
        count = 0
        for i in range(int(len(desc_list) / 2)):
            desc_info = {
                desc_list[count]: desc_list[count+1]
            }
            desc_data.append(desc_info)
            count += 2
        item['description'] = desc_data
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
