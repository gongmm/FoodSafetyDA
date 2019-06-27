# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShipinItem(scrapy.Item):
    time=scrapy.Field()
    link=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    category=scrapy.Field()
    tags=scrapy.Field()
    area=scrapy.Field()

