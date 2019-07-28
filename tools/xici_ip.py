"""
    create by Gray 2019-07-18
"""
import time

import requests
from scrapy.selector import Selector
import pymysql


db_connect = pymysql.connect(host='localhost',
                             port=8889,
                             db='article_spider',
                             user='root',
                             passwd='123456',
                             charset='utf8mb4')
cursor = db_connect.cursor()


def crawl_ip():
    # 爬取西刺免费ip
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    for i in range(1, 51):
        re = requests.get('https://www.xicidaili.com/nn/{}'.format(i), headers=headers)

        selector = Selector(text=re.text)

        all_trs = selector.css('#ip_list tr')

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract_first('')
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            else:
                speed = 0

            all_texts = tr.css('td::text').extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        insert_sql = """
                     INSERT INTO proxy_ip(ip, port, proxy_type, speed) 
                     VALUES (%s, %s, %s, %s)
                     ON DUPLICATE KEY UPDATE port=VALUES(port), speed=VALUES(speed);
        """
        for ip_info in ip_list:
            print(ip_info)
            cursor.execute(insert_sql, ip_info)
            db_connect.commit()

        time.sleep(3)


crawl_ip()
