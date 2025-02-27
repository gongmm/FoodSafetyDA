# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    keyword = scrapy.Field()
    url = scrapy.Field()
    pubdate = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    # digest=scrapy.Field()
