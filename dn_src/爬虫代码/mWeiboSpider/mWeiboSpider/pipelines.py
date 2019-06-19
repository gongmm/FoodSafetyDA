# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from mWeiboSpider.items import weibospiderItem
class MweibospiderPipeline(object):
    def open_spider(self, spider):
        self.db = MongoClient(host="127.0.0.1", port=27017)
        self.client = self.db.Sina.weibonew3

    def process_item(self, item, spider):
        if isinstance(item, weibospiderItem):
            self.client.update_one({'content':item['content']},{'$set':dict(item)},upsert=True)
        return item
