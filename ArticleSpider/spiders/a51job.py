# -*- coding: utf-8 -*-
import datetime

import requests
import scrapy
from scrapy import Selector

from ArticleSpider.items import ArticleItemLoader, A51jobItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        jobs_nodes = response.css("#resultList .el .t1 a::attr(href)").extract()
        headers = {
            'Host': 'jobs.51job.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        for job_url in jobs_nodes:
            yield scrapy.Request(job_url, headers=headers, dont_filter=True, callback=self.parse_detail)

        # 下一页
        next_node = response.css(".dw_page .bk")[1]
        next_url = next_node.css("a::attr(href)").extract_first('')
        if next_url:
            yield scrapy.Request(next_url, dont_filter=True, callback=self.parse)

    def parse_detail(self, response):
        msg_list = response.css(".tHeader .msg.ltype::text").extract()
        work_year = msg_list[1].strip()
        education = msg_list[2].strip()
        city = msg_list[0].strip()

        jobid = response.css("#hidJobID::attr(value)").extract()[0]

        longitude, latitude = self.get_coordinate(jobid)

        item_loader = ArticleItemLoader(item=A51jobItem(), response=response)
        item_loader.add_css('positionID', "#hidJobID::attr(value)")
        item_loader.add_css('positionName', ".tCompany_center .tHeader h1::attr(title)")
        item_loader.add_css('salary', ".tHeader .in .cn strong::text")
        item_loader.add_value('workYear', work_year)
        item_loader.add_value('education', education)
        item_loader.add_value('city', city)
        item_loader.add_xpath('financeStage', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[1]/text()")
        item_loader.add_xpath('companySize', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[2]/text()")
        item_loader.add_css('companyName', ".cname .catn::attr(title)")
        item_loader.add_xpath('industryField', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[3]/@title")
        item_loader.add_value('longitude', longitude)
        item_loader.add_value('latitude', latitude)
        item_loader.add_value('crawl_date', datetime.date.today())

        job_item = item_loader.load_item()

        yield job_item

    def get_coordinate(self, jobid):
        # 获取经纬度
        map_url = 'https://search.51job.com/jobsearch/bmap/map.php?jobid={}'.format(jobid)
        res = requests.get(map_url)
        res_selector = Selector(response=res)
        longitude = res_selector.css("#end::attr(lng)").extract()[0]
        latitude = res_selector.css("#end::attr(lat)").extract()[0]
        return longitude, latitude
