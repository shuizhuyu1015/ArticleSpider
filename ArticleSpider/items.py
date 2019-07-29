# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

from ArticleSpider.utils.common import date_convert, get_nums


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def remove_comment_tags(value):
    # 去掉tags中的评论
    if "评论" in value:
        return ''
    else:
        return value


def return_value(value):
    return value


def get_jiuyi_tags(value):
    tags = ''
    if 'dujia' in value:
        tags = '独家'
    elif 'xinwen' in value:
        tags = '新闻'
    elif 'muying' in value:
        tags = '母婴'
    elif 'yangsheng' in value:
        tags = '养生'
    elif 'yimei' in value:
        tags = '医美'
    elif 'liangxing' in value:
        tags = '两性'
    elif 'yundong' in value:
        tags = '运动'
    elif 'wenda' in value:
        tags = '问答'
    elif 'yishengshuo' in value:
        tags = '医生说'
    elif 'yinghe' in value:
        tags = '基因'
    return tags


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert, date_format="%Y/%m/%d")
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
    publish_date = scrapy.Field(
        input_processor=MapCompose(date_convert, date_format="%Y-%m-%d %H:%M:%S")
    )
    check_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(get_jiuyi_tags)
    )

    def get_insert_sql(self):
        insert_sql = """
                        insert into jiuyi160_article(title, url, url_id, front_image_url, front_image_path, publish_date, check_num, content, tags)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE check_num=VALUES(check_num), publish_date=VALUES (publish_date);
                    """
        params = (
            self.get("title", ''),
            self.get("url", ''),
            self.get('url_id', ''),
            self.get("front_image_url", ''),
            self.get("front_image_path", ''),
            self.get('publish_date', ''),
            self.get('check_num', 0),
            self.get('content', ''),
            self.get('tags', '')
        )
        return insert_sql, params


class NewrankArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    publish_time = scrapy.Field(
        input_processor=MapCompose(date_convert, date_format="%Y-%m-%d %H:%M:%S")
    )
    buy_count = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )

    def get_insert_sql(self):
        insert_sql = """
                        insert into newrank(title, url, url_id, author, tag, publish_time, buy_count)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE buy_count=VALUES(buy_count);
                    """
        params = (
            self.get("title", ''),
            self.get("url", ''),
            self.get('url_id', ''),
            self.get("author", ''),
            self.get("tag", ''),
            self.get('publish_time', ''),
            self.get('buy_count', 0)
        )
        return insert_sql, params


class A51jobItem(scrapy.Item):
    # 岗位ID,非空字段
    positionID = scrapy.Field()
    # 岗位名称
    positionName = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 工作年限
    workYear = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 岗位性质（全职兼职）
    jobNature = scrapy.Field()
    # 公司类型（是否融资）
    financeStage = scrapy.Field()
    # 公司规模
    companySize = scrapy.Field()
    # 公司名称
    companyName = scrapy.Field()
    # 业务方向
    industryField = scrapy.Field()
    # 经度
    longitude = scrapy.Field()
    # 纬度
    latitude = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 抓取日期
    crawl_date = scrapy.Field()
