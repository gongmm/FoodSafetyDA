# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
from pymongo import MongoClient
from News.items import NewsItem


class FoodMateDatabasePipeline(object):
    def open_spider(self, spider):
        self.conn = MongoClient(host='127.0.0.1', port=27017)
        self.client = self.conn.news.thepaper

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            self.client.update({'url': item['url']}, {'$set': dict(item)}, True)
            # self.client.insert(dict(item))
            return item


class NewsWBPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['keyword', 'url', 'pubdate', 'title', 'content'])

    def process_item(self, item, spider):  # 工序具体内容
        if isinstance(item, NewsItem):
            # 导出表格操作
            line = [item['keyword'], item['url'], item['pubdate'], item['title'], item['content']]  # 把数据每一行整理出来
            self.ws.append(line)  # 将数据一行的形式添加到xlsx中
            self.wb.save('news.xlsx')  # 保存xlsx文件
            return item
