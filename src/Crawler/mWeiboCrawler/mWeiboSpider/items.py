# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiBoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topic = scrapy.Field()
    topic_id = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    reposts_count = scrapy.Field()  # 转发数
    comments_count = scrapy.Field()  # 评论数
    attitudes_count = scrapy.Field()  # 点赞数
    pass
