# -*- coding: utf-8 -*-
import json
import re
from urllib import parse

import scrapy


class CodingkeSpider(scrapy.Spider):
    # 练习登录后采集数据
    name = 'codingke'
    allowed_domains = ['www.codingke.com']
    start_urls = ['http://www.codingke.com/my']

    headers = {
        'Host': 'www.codingke.com',
        'Referer': 'http://www.codingke.com/login',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    def start_requests(self):
        return [scrapy.Request('http://www.codingke.com/login', callback=self.login)]

    def login(self, response):
        # 本想通过css()获取meta的值，但是发现只有scrapy自带的parse方法才能使用response.css()或xpath方法，只能正则了
        response_text = response.text
        match_obj = re.match('.*meta content="(.*?)" name="csrf-token"', response_text, re.DOTALL)
        csrf = ''
        if match_obj:
            csrf = match_obj.group(1)

        if csrf:
            post_data = {
                '_username': '18666278637',
                '_password': 'shuizhuyu1015',
                '_csrf_token': csrf
            }
            # 多次调试后发现需要传入headers，且需加入以下两个header字段
            headers = self.headers
            headers['X-CSRF-Token'] = csrf
            headers['X-Requested-With'] = 'XMLHttpRequest'
            return [scrapy.FormRequest(url='http://www.codingke.com/login_check',
                                       headers=self.headers,
                                       formdata=post_data,
                                       callback=self.login_check)]

    def login_check(self, response):
        text_json = json.loads(response.text)
        if text_json['success']:
            for url in self.start_urls:
                yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        course_list = response.css(".uc_course_list li")
        items = []
        for course in course_list:
            course_name = course.css("p a[class='name']::text").extract_first('')
            course_url = course.css("a::attr(href)").extract_first('')
            study_progress = course.css("p[class='pro1'] span::text").extract_first('')
            item = {
                'course_name': course_name,
                'course_url': parse.urljoin(response.url, course_url),
                'study_progress': study_progress
            }
            items.append(item)
        print(items)
