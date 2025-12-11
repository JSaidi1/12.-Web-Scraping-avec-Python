# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



import re

class CleanPricePipeline:
    def process_item(self, item, spider):
        item['price'] = float(re.sub(r'[£]', '', item['price']))
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.ids_seen:
            raise scrapy.exceptions.DropItem(f"Duplicate item found: {item['title']}")
        else:
            self.ids_seen.add(item['title'])
            return item

