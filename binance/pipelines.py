# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class BinancePipeline(object):
    def process_item(self, item, spider):

        completed = item['completed']
        tokens = completed.split("%", 1)
        try:
            completed = float(tokens[0].replace(",", ""))
        except:
            completed = 0.0
        item['completed'] = completed


        try:
            item['price'] = float(item['price'].replace(",", ""))
        except:
            pass

        try:
            available = item['available']
            tokens = available.split(" ", 1)
            item["available"] = float(tokens[0].replace(",", ""))
        except:
            pass


        try:
            available = item['order_count']
            tokens = available.split(" ", 1)
            item["order_count"] = int(tokens[0].replace(",", ""))
        except:
            pass



        try:
            item["low_limit"] = float(item['low_limit'].replace(",", ""))
        except:
            pass



        try:
            item["high_limit"] = float(item['high_limit'].replace(",", ""))
        except:
            pass



        return item

class MongoDBPipeline(object):
    # def __init__(self):
    #     self. connection = pymongo.MongoClient(
    #         settings['MONGODB_URI']
    #     )

    #     self.db = self.connection[settings['MONGODB_DB']]
    #     self.collection = self.db[settings['MONGODB_COLLECTION']]

    # @classmethod
    # def from_crawler(cls, crawler):
    #     pass

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_URI']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.collection.insert(item)
        return item
