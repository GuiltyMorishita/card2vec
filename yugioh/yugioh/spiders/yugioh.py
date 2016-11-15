# -*- coding: utf-8 -*-
import scrapy
from ..items import YugiohItem
from bs4 import BeautifulSoup
from more_itertools import chunked
import re

class YugiohSpider(scrapy.Spider):
    name = "yugioh"
    allowed_domains = ["yugioh-list.com"]
    root_url = 'http://yugioh-list.com'

    def start_requests(self):
        yield scrapy.Request(self.root_url + "/c_lists", callback=self.start_requests_parse)

    def start_requests_parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        url_list = []
        for link in soup.findAll("a"):
            href = link.get("href")
            if re.search(r"/p_dtls/index/\d+", href):
                url = self.root_url + href
                url_list.append(url)
        target_urls = set(url_list)
        for target_url in target_urls:
            yield scrapy.Request(target_url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        title = soup.find("div", class_="pack_detail").find("img").get("title")
        print(title)
        table_rows = soup.find("table", class_="tableList scroll-box").findAll("tr")
        card_rows = table_rows[1:-1]
        for upper, lower in chunked(card_rows, 2):
            item = YugiohItem()
            item['name'] = upper.findAll("td")[3].text.rstrip()
            item['text'] = lower.find("span").text.rstrip()
            yield item
