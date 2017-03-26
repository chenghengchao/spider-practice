# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YzdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    general_name = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    scale = scrapy.Field()
    rate = scrapy.Field()
    danwei = scrapy.Field()
    price = scrapy.Field()
    quality = scrapy.Field()
    pro_com = scrapy.Field()
    tou_com = scrapy.Field()
    province = scrapy.Field()
    date = scrapy.Field()
    beizhu = scrapy.Field()
    file = scrapy.Field()
    file_link = scrapy.Field()
    product = scrapy.Field()
