# -*- coding: utf-8 -*-

import scrapy


class HearthStoneItem(scrapy.Item):
    name = scrapy.Field()
    rarity = scrapy.Field()
    ruby = scrapy.Field()
    type = scrapy.Field()
    hero = scrapy.Field()
    race = scrapy.Field()
    card_text = scrapy.Field()
    mana = scrapy.Field()
    attack = scrapy.Field()
    health = scrapy.Field()
