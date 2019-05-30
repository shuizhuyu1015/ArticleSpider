# -*- coding: utf-8 -*-
import scrapy


class NewrankZczSpider(scrapy.Spider):
    name = 'newrank_zcz'
    allowed_domains = ['cc.newrank.cn']
    start_urls = ['https://cc.newrank.cn/content-management.html']

    def parse(self, response):
        post_urls = response.css("div.table-row-div").extract()
        pass
