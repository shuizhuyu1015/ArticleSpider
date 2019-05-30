# -*- coding: utf-8 -*-
from urllib import parse
import scrapy


class Jiuyi160Spider(scrapy.Spider):
    name = 'jiuyi160'
    allowed_domains = ['news.91160.com']
    start_urls = ['https://news.91160.com/dujia/']

    headers = {
        'Host': 'news.91160.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        post_nodes = response.css(".lists li a")
        for post_node in post_nodes:
            image_url = post_nodes.css("img::attr(src)").extract_first('')
            post_url = post_node.css("::attr(href)").extract_first('')
            yield scrapy.Request(url=parse.urljoin(response.url, post_url),
                                 meta={'front_image_url': image_url},
                                 headers=self.headers,
                                 callback=self.parse_detail)
        # 下一页
        last_next_nodes = response.css(".consola")
        if last_next_nodes:
            # .consola选择器有可能会获取到2个，一个上一页，一个下一页，有两个时后一个为下一页
            next_node = last_next_nodes[1] if len(last_next_nodes) > 1 else last_next_nodes[0]
            next_url = next_node.css("::attr(href)").extract_first('')
            next_url = parse.urljoin(response.url, next_url)
            next_headers = self.headers
            next_headers['Referer'] = response.url
            yield scrapy.Request(url=next_url, headers=next_headers, callback=self.parse)

    def parse_detail(self, response):
        pass
