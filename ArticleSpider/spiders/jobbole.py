# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader

from ArticleSpider.items import JobboleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 解析列表页所有文章URL，并交给scrapy下载解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 文章封面图
            image_url = post_node.css("img::attr(src)").extract_first('')
            # 文章URL
            post_url = post_node.css("::attr(href)").extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first('')
        if next_url:
            # 正式爬取数据需将以下post_url换为next_url，否则无法爬取下一页
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobboleArticleItem()

        """
        通过xpath提取，
        优点：debug可查看出错的xpath表达式错误原因，
        缺点：表达式比较长
        """
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first('')
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first('').\
        #     strip().replace('·', '').strip()
        # # 点赞
        # support_num = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first('')
        # # 收藏
        # collect_num = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first('').strip()
        # reg_str = ".*?(\d+).*"
        # match_re = re.match(reg_str, collect_num)
        # if match_re:
        #     collect_num = match_re.group(1)
        # # 评论
        # comment_num = response.xpath("//a[@href='#article-comment']/span[contains(@class, 'btn-bluet-bigger')]/text()")\
        #     .extract_first('')
        # match_re = re.match(reg_str, comment_num)
        # if match_re:
        #     comment_num = match_re.group(1)
        #
        # content = response.xpath("//div[@class='entry']").extract_first('')
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        # tag_list = ','.join(tag_list)


        """
        通过css选择器提取，
        缺点：debug无法查看出错的css提取表达式错误原因，
        优点：但css表达式简洁，与前端语言匹配
        """
        front_image_url = response.meta.get('front_image_url', '')
        # title = response.css(".entry-header h1::text").extract_first('')
        # create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first('').\
        #     strip().replace('·', '').strip()
        #
        # praise_num = int(response.css(".vote-post-up h10::text").extract_first(''))
        #
        # collect_num = response.css(".bookmark-btn::text").extract_first('').strip()
        # reg_num = ".*?(\d+).*"
        # match_re = re.match(reg_num, collect_num)
        # if match_re:
        #     collect_num = int(match_re.group(1))
        # else:
        #     collect_num = 0
        #
        # comment_num = response.css("a[href='#article-comment'] span::text").extract_first('')
        # match_re = re.match(reg_num, comment_num)
        # if match_re:
        #     comment_num = int(match_re.group(1))
        # else:
        #     comment_num = 0
        #
        # content = response.css(".entry").extract_first('')
        #
        tag_list = response.css(".entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)
        #
        # article_item['title'] = title
        # article_item['url'] = response.url
        # article_item['url_object_id'] = get_md5(response.url)
        # try:
        #     create_date = datetime.datetime.strftime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_num'] = praise_num
        # article_item['comment_num'] = comment_num
        # article_item['collect_num'] = collect_num
        # article_item['content'] = content
        # article_item['tags'] = tags


        """
        通过itemloader加载item
        """
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css('title', ".entry-header h1::text")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', ".entry-meta-hide-on-mobile::text")
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_num', "span.vote-post-up h10::text")
        item_loader.add_css('comment_num', "a[href='#article-comment'] span::text")
        item_loader.add_css('collect_num', "span.bookmark-btn::text")
        item_loader.add_css('content', ".entry")
        item_loader.add_value('tags', tags)

        article_item = item_loader.load_item()

        yield article_item
