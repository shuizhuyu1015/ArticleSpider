# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from datetime import datetime
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        value = value.strip().replace('·', '').strip()
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date


def get_nums(value):
    reg_num = ".*?(\d+).*"
    match_re = re.match(reg_num, value.strip())
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉tags中的评论
    if "评论" in value:
        return ''
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    collect_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        insert into jobbole(title, url, url_object_id, create_date, collect_num, comment_num, praise_num, front_image_url, tags, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE collect_num=VALUES(collect_num), comment_num=VALUES(comment_num), praise_num=VALUES(praise_num);
                    """
        params = (
            self.get("title", ''),
            self.get("url", ''),
            self.get('url_object_id', ''),
            self.get("create_date", ''),
            self.get("collect_num", 0),
            self.get('comment_num', 0),
            self.get('praise_num', 0),
            self.get('front_image_url', ''),
            self.get('tags', ''),
            self.get('content', '')
        )
        return insert_sql, params


class Jiuyi160ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    publish_date = scrapy.Field()
    check_num = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        insert into jobbole_article(title, url, url_id, front_image_url, front_image_path, publish_date, check_num, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE check_num=VALUES(check_num);
                    """
        params = (
            self.get("title", ''),
            self.get("url", ''),
            self.get('url_id', ''),
            self.get("front_image_url", ''),
            self.get("front_image_path", ''),
            self.get('publish_date', ''),
            self.get('check_num', 0),
            self.get('content', '')
        )
        return insert_sql, params
