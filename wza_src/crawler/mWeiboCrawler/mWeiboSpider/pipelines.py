# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from pymongo import MongoClient
from mWeiboSpider.items import WeiBoSpiderItem
from openpyxl import Workbook


class MWeiBoSpiderPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['time', 'content', 'topic_id', 'topic', 'reposts_count', 'comments_count', 'attitudes_count'])

    def process_item(self, item, spider):  # 工序具体内容
        if isinstance(item, WeiBoSpiderItem):
            # 导出表格操作
            line = [item['time'], item['content'], item['topic_id'], item['topic'], item['reposts_count'],
                    item['comments_count'], item['attitudes_count']]  # 把数据每一行整理出来
            self.ws.append(line)  # 将数据一行的形式添加到xlsx中
            self.wb.save('weibo.xlsx')  # 保存xlsx文件
            return item


# class MWeiBoDatabasePipeline(object):
#     def open_spider(self, spider):
#         self.db = MongoClient(host="127.0.0.1", port=27017)
#         self.client = self.db.Sina.weibonew3
#
#     def process_item(self, item, spider):
#         if isinstance(item, weibospiderItem):
#             self.client.update_one({'content': item['content']}, {'$set': dict(item)}, upsert=True)
#         return item
