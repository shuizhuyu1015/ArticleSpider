"""
    create by Gray 2019-07-18
"""
import time

import requests
from scrapy.selector import Selector
import pymysql


class Xici:
    def __init__(self):
        self.db_connect = pymysql.connect(host='localhost',
                                     port=8889,
                                     db='article_spider',
                                     user='root',
                                     passwd='123456',
                                     charset='utf8mb4')
        self.cursor = self.db_connect.cursor()

    def crawl_ip(self):
        # 爬取西刺免费ip
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        for i in range(1, 11):
            re = requests.get('https://www.xicidaili.com/wn/{}'.format(i), headers=headers)

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

            # 保存到数据库
            insert_sql = """
                         INSERT INTO proxy_ip(ip, port, proxy_type, speed) 
                         VALUES (%s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE port=VALUES(port), speed=VALUES(speed);
            """
            for ip_info in ip_list:
                self.cursor.execute(insert_sql, ip_info)
                self.db_connect.commit()

            time.sleep(3)

    def get_random_ip(self):
        # 从数据库随机获取一个可用IP
        random_sql = """
            SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1;
        """
        self.cursor.execute(random_sql)
        for ip_info in self.cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge_result = self.__judge_ip(ip, port)
            if judge_result:
                return 'https:{}:{}'.format(ip, port)
            else:
                return self.get_random_ip()

    def __judge_ip(self, ip, port):
        # 判断ip是否可用
        https_url = 'https://www.baidu.com'
        proxy_url = 'https://{0}:{1}'.format(ip, port)
        try:
            proxy_dict = {
                'https': proxy_url
            }
            res = requests.get(https_url, proxies=proxy_dict)
        except Exception as e:
            print('invalid ip:{0} and port:{1}'.format(ip, port))
            self.__delete_ip(ip)
            return False
        else:
            code = res.status_code
            if code >= 200 and code < 300:
                print('effective ip')
                return True
            else:
                print('invalid ip:{0} and port:{1}'.format(ip, port))
                self.__delete_ip(ip)
                return False

    def __delete_ip(self, ip):
        delete_sql = """
            delete from proxy_ip where ip = %s;
        """
        self.cursor.execute(delete_sql, ip)
        self.db_connect.commit()


if __name__ == '__main__':
    xici = Xici()
    # xici.crawl_ip()
    random_ip = xici.get_random_ip()
    print(random_ip)
