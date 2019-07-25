# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from zhihu.items import ZhiHuItem
from zhihu.settings import filename
import csv
import os


class ZhihuPipeline(object):
    # def __init__(self):
    # csv文件的位置,无需事先创建
    # store_file = os.path.dirname(__file__) + '/spiders/articles.csv'
    # print("***************************************************************")
    # # 打开(创建)文件
    #
    # self.file = open(filename, 'a+', encoding="utf-8",newline = '')
    # # csv写法
    # self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        print("正在写入......")
        # if item['article_title']:
        # 主要是解决存入csv文件时出现的每一个字以‘，’隔离
        with open(filename, 'a+', encoding='utf-8', newline='') as f:
            # f = open(filename,'a+',encoding='utf-8',newline = '')
            writer = csv.writer(f, dialect="excel")
            writer.writerow([item['keyword'], item['question'], item['content'], item['pub_date']])
            return item
