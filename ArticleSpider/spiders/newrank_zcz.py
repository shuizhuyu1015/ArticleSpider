# -*- coding: utf-8 -*-
from urllib import parse
import time

import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, Selector
from ArticleSpider.items import ArticleItemLoader, NewrankArticleItem
from ArticleSpider.utils.common import get_md5


class NewrankZczSpider(scrapy.Spider):
    name = 'newrank_zcz'
    allowed_domains = ['cc.newrank.cn']
    start_urls = ['https://cc.newrank.cn/content-management.html']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='/Users/tianguanjia/Downloads/chromedriver')
        super(NewrankZczSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 当爬虫退出时关闭Chrome
        self.browser.quit()

    def start_requests(self):
        return [scrapy.Request('https://www.newrank.cn/public/login/login.html', callback=self.login)]

    def login(self, response):
        self.browser.find_element_by_css_selector("div.login-normal-tap[data-type='pwd']").click()
        self.browser.find_element_by_css_selector("#account_input").send_keys('18050932862')
        self.browser.find_element_by_css_selector("#password_input").send_keys('Zcz123456')
        self.browser.find_element_by_css_selector("#pwd_confirm").click()
        time.sleep(2)
        for url in self.start_urls:
            yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        if 'content-management' in response.url:
            list_nodes = response.css("div.table-row-div .list-row")
            for list_node in list_nodes:
                data_url = list_node.css("::attr(data-url)").extract_first('')
                item_loader = ArticleItemLoader(item=NewrankArticleItem(), selector=list_node)
                item_loader.add_value("url", data_url)
                item_loader.add_value("url_id", get_md5(data_url))
                item_loader.add_css("title", ".article .title::text")
                item_loader.add_css("author", ".author .account::text")
                item_loader.add_css("tag", ".tag::text")
                item_loader.add_css("publish_time", ".start-time::text")
                item_loader.add_css("buy_count", ".buy-count::text")

                article_item = item_loader.load_item()
                yield article_item

            next_page = response.xpath("//div[@id='pager']/span[@class='pagebar-link']/a").extract()[2]
            if next_page:
                t_selector = Selector(text=self.browser.page_source)
                cur = int(t_selector.css(".cur::text").extract_first(1))
                yield scrapy.Request(response.url, meta={'current_page': cur+1}, dont_filter=True, callback=self.parse)
