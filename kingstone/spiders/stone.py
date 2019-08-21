# -*- coding: utf-8 -*-
import scrapy
from kingstone.items import KingstoneItem
import re

class tag_collecting(scrapy.Spider):
    name = 'tag_collecting'
    allowed_domains = ['www.kingstone.com.tw']
    start_urls = ['https://www.kingstone.com.tw/new/mag/'] # 雜誌

    def parse(self, response):
        print(response.url) # <200 https://www.kingstone.com.tw/new/mag/>
        final_list = [] # 包含域名(包含雜誌) + 類別1_iiiiq + qa + id
        if response.url == self.start_urls[0]:
            # 獲得所有iiiiq....
            hxs = scrapy.selector.HtmlXPathSelector(response)
            hlist = hxs.select('.//li/a[contains(@href,"new/mag")]/@href').extract() # contains包含@代表屬性，"代表文字" 很方便
            for x in hlist:
                url = "https://www.kingstone.com.tw"+x
                yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
        if "new/mag/iiii" in response.url:
            # 獲得所有qa,b,c,d,e,f,g....
            hxs = scrapy.selector.HtmlXPathSelector(response)
            hlist_2 = hxs.select('.//nav[@class="navcolumn_classlevel"]/ul/li/ul/li/a/@href').extract()
            for x in hlist_2:
                url = "https://www.kingstone.com.tw"+x
                yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
        if "/mag/mag_class.asp" in response.url:
            # 獲得所有id....
            hxs = scrapy.selector.HtmlXPathSelector(response)
            hlist_3 = hxs.select('.//a[contains(@href,"new/basic")]/@href').re(r'/new/basic/([0-9]+)?')
            item = KingstoneItem()
            for vo in hlist_3:
                item['url'] = "https://www.kingstone.com.tw/new/basic/"+vo
            yield item
            
            next_page = re.findall(r'<a href="/mag/mag_class.asp.*?class_id=(\w+).*?&page=([0-9]+).*?下一頁',response.text)
            if next_page:
                next_url = "https://www.kingstone.com.tw/mag/mag_class.asp?class_id="+next_page[0][0]+"&act_class=0&page="+next_page[0][1]
                url = response.urljoin(next_url)
                yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    