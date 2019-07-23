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
    pass
