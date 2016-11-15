# -*- coding: utf-8 -*-
import scrapy


class YugiohItem(scrapy.Item):
    name = scrapy.Field()
    text = scrapy.Field()
