# -*- coding: utf-8 -*-
import scrapy
from ..items import HearthStoneItem
from bs4 import BeautifulSoup


class HearthStoneSpiderSpider(scrapy.Spider):
    name = "hearth_stone_spider"
    allowed_domains = ["4gamer.net"]
    start_urls = ['http://www.4gamer.net/games/209/G020915/FC20140702001/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        for card in soup.find("div", id="UNIT_LIST").findAll("div"):
            item = HearthStoneItem()
            item['name'] = card.find("span", class_="name").string
            item['rarity'] = card.find("span", class_="rarity").string
            item['ruby'] = card.find("span", class_="ruby").string
            item['type'] = card.find("span", class_="type").string
            item['hero'] = card.find("span", class_="class").string
            item['race'] = card.find("span", class_="race").string
            item['card_text'] = card.find("span", class_="card_comment").find("p").string
            item['mana'] = card.find("span", class_="mana").string
            item['attack'] = card.find("span", class_="attack").string
            item['health'] = card.find("span", class_="health").string
            yield item
