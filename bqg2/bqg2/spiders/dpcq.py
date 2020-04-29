# -*- coding: utf-8 -*-
import scrapy
from bqg2.items import Bqg2Item

class DpcqSpider(scrapy.Spider):
    name = 'dpcq'
    allowed_domains = ['www.52bqg.com']
    start_urls = ['https://www.52bqg.com/book_127354/']

    def parse(self, response):
        # item = Bqg2Item()
        list1=response.xpath('//*[@id="list"]/dl/dd/a')
        for each in list1:
            urltxt=each.xpath('@href').extract()[0]
            # ml=each.xpath('text()').extract()
            # item["ml"]=ml[0]
            yield response.follow(urltxt,callback=self.parse1)

    def parse1(self, response):
        item=Bqg2Item()
        txt=response.xpath('//*[@id="content"]/text()').extract()
        item["ml"] = response.xpath('//*[@id="box_con"]/div[2]/h1/text()').extract()
        item["txt"]="".join(txt).replace(" ","").replace("\r\n","")
        yield item







