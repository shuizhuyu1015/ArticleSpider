# -*- coding: utf-8 -*-
import scrapy

from ArticleSpider.items import ArticleItemLoader, A51jobItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['search.51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        jobs_nodes = response.css("#resultList .el .t1 a::attr(href)").extract()
        for job_url in jobs_nodes:
            yield scrapy.Request(job_url, dont_filter=True, callback=self.parse_detail)

    def parse_detail(self, response):
        item_loader = ArticleItemLoader(item=A51jobItem(), response=response)
        item_loader.add_css('positionID', "#hidJobID::attr(value)")
        item_loader.add_css('positionName', ".tCompany_center .tHeader h1::attr(title)")
        item_loader.add_css('salary', ".tHeader .in .cn strong::text")
        item_loader.add_css('workYear', ".tHeader .msg.ltype::text")
        item_loader.add_xpath('financeStage', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[1]/text()")
        item_loader.add_xpath('companySize', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[2]/text()")
        item_loader.add_css('companyName', ".cname .catn::attr(title)")
        item_loader.add_xpath('industryField', "//div[@class='tBorderTop_box']/div[@class='com_tag']/p[3]/@title")

        job_item = item_loader.load_item()

        yield job_item
