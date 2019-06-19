    # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo



class ShipinspiderPipeline(object):
    #初始化mongodb数据库
    def __init__(self,mongo_host,mongo_port,mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db


    @classmethod
    #读取settings里mongodb的host,port,bdname
    def from_crawler(cls,crawler):
        return cls(
            mongo_host = crawler.settings.get("MONGODB_HOST"),
            mongo_port = crawler.settings.get("MONGODB_PORT"),
            mongo_db = crawler.settings.get("MONGODB_DBNAME"),

        )
    #连接mongodb
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_host,self.mongo_port)
        self.db = self.client[self.mongo_db]

    #将数据写入数据库
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
