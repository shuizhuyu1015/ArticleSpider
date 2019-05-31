# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
from ArticleSpider.items import ArticleItemLoader, Jiuyi160ArticleItem
from ArticleSpider.utils.common import get_md5


class Jiuyi160Spider(scrapy.Spider):
    name = 'jiuyi160'
    allowed_domains = ['news.91160.com']
    start_urls = [
        # 'https://news.91160.com/dujia/',
        # 'https://news.91160.com/xinwen/',
        'https://news.91160.com/muying/beiyun/',
        'https://news.91160.com/muying/huaiyun/',
        'https://news.91160.com/muying/xinshenger/',
        'https://news.91160.com/muying/youer/',
        # 'https://news.91160.com/yangsheng/',
        'https://news.91160.com/yimei/wuguan/',
        'https://news.91160.com/yimei/meifu/',
        # 'https://news.91160.com/liangxing/',
        # 'https://news.91160.com/yundong/',
        # 'https://news.91160.com/yishengshuo/',
        # 'https://news.91160.com/wenda/',
        # 'https://news.91160.com/yinghe/'
    ]

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
        item_loader = ArticleItemLoader(item=Jiuyi160ArticleItem(), response=response)
        item_loader.add_css("title", ".detail_title::text")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_id', get_md5(response.url))
        item_loader.add_value('front_image_url', response.meta.get('front_image_url', ''))
        item_loader.add_css('publish_date', ".mr20.v_middle::text")
        item_loader.add_css('check_num', "#click::text")
        item_loader.add_css('content', ".articel")
        item_loader.add_value('tags', response.url)

        article_item = item_loader.load_item()
        yield article_item
