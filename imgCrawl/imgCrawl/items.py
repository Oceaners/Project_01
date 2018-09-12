# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 图片地址
    img_url = scrapy.Field()
    # 图片描述
    img_title = scrapy.Field()
