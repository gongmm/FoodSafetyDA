# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ShipinspiderItem(scrapy.Item):
    keyword = Field()  # 搜索关键词
    title = Field()  # 标题
    pubdate = Field()  # 发布时间
    source = Field()  # 视频源地址
