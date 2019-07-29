# -*- coding: utf-8 -*-
import json

import requests
import scrapy


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    keyword = 'Python'
    lagou_session = requests.session()

    def start_requests(self):
        all_city_url = 'https://www.lagou.com/jobs/allCity.html'
        return [scrapy.Request(all_city_url, headers=self.headers, callback=self.get_all_citys)]

    def get_all_citys(self, response):
        all_citys = response.css(".word_list .city_list a::text").extract()
        for city in all_citys:
            job_url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(city)
            data = {
                'first': True,
                'pn': 1,
                'kd': self.keyword
            }
            self.headers['Referer'] = 'https://www.lagou.com/jobs/list_ios?px=default&city={}'.format(city).encode()

            cookies = 'JSESSIONID=ABAAABAAAIAACBI55DD7C5E5DF07849446FE53DEE73CC8B; WEBTJ-ID=20190726173948-16c2da698fd231-0186e66f5ab114-37607c05-2073600-16c2da698fe278; _ga=GA1.2.1332843887.1564133989; user_trace_token=20190726173949-4f81dbb8-af89-11e9-8411-525400f775ce; LGUID=20190726173949-4f81dfef-af89-11e9-8411-525400f775ce; TG-TRACK-CODE=index_search; _gid=GA1.2.1309589319.1564371554; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1564133989,1564371555; X_MIDDLE_TOKEN=fffdd48ddc373f081f0e0d347de7fc2c; index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=11bc755ac04c44e6b4ff766df6d47936; LGSID=20190729141909-c6cdd026-b1c8-11e9-8562-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Futrack%2FtrackMid.html%3Ff%3Dhttps%253A%252F%252Fwww.lagou.com%252Fjobs%252Flist%255FiOS%253Fcity%253D%2525E6%2525B7%2525B1%2525E5%25259C%2525B3%2526cl%253Dfalse%2526fromSearch%253Dtrue%2526labelWords%253D%2526suginput%253D%26t%3D1564381147%26_ti%3D14; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_iOS%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; X_HTTP_TOKEN=376fd609557696e17312834651b956ecd9ab8130bd; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1564382138; LGRID=20190729143538-13df953a-b1cb-11e9-a4f6-5254005c3644'
            cookies = {i.split("=")[0].strip(): i.split("=")[1].strip() for i in cookies.split("; ")}

            yield scrapy.Request(job_url, method='POST', headers=self.headers, body=json.dumps(data))

    def parse(self, response):
        title = response.css('title')
        print(title)
