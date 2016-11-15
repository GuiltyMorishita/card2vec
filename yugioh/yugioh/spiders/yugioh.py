# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from ..items import YugiohItem
from bs4 import BeautifulSoup
from more_itertools import chunked
import re

class YugiohSpider(scrapy.Spider):
    name = "yugioh"
    allowed_domains = ["ocg-card.com"]
    start_urls = ['http://ocg-card.com/list/']

    rules = [
        Rule(LinkExtractor(allow=r"/list/list"), follow=True),
        Rule(LinkExtractor(allow=r"/list/list", unique=True), callback="parse")
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        table_rows = soup.find("table", border=2).findAll("tr")
        # cards = [(i+j) for (i, j) in zip(table_rows[::2], table_rows[1::2])]
        del(table_rows[0])
        for upper, lower in chunked(table_rows, 2):
            item = YugiohItem()
            item['name'] = upper.findAll("td")[1].text
            item['text'] = lower.find("td").text
            yield item
