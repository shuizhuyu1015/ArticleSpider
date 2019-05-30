# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 为了获取下载图片的路径，可继承ImagesPipeline自定义图片下载管道，获取图片路径
    def item_completed(self, results, item, info):
        if 'front_image_path' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path

        return item


class JsonWithEncodingPipeline:
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self):
        self.file.close()


class JsonExporterPipeline:
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleExport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline:
    # 同步加载数据库
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.db_cur = db_conn.cursor()

    @classmethod
    def from_settings(cls, settings):
        db = settings.get('MYSQL_DBNAME', 'article_spider')
        host = settings.get('MYSQL_HOST', 'localhost')
        port = settings.get('MYSQL_PORT', 8889)
        user = settings.get('MYSQL_USER', 'root')
        passwd = settings.get('MYSQL_PASSWORD', '123456')
        db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        return cls(db_conn)

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cur.close()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    # 插入数据
    def insert_db(self, item):
        values = (
            item['title'],
            item['url'],
            item['url_object_id'],
            item['create_date'],
            item.get('praise_num', 0),
            item.get('collect_num', 0),
            item.get('comment_num', 0),
            item['tags']
        )
        try:
            sql = """
                    insert into jobbole (title, url, url_object_id, create_date, praise_num, collect_num,comment_num,tags)
                    values (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.db_conn.ping(reconnect=True)
            self.db_cur.execute(sql, values)
            self.db_conn.commit()
            print("Insert finished")
        except Exception as e:
            print(e)
            self.db_conn.commit()
            self.db_conn.close()


class MysqlTwistedPipline(object):
    # 异步加载数据库
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            port=settings['MYSQL_PORT'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
