# -*- coding: utf-8 -*-
import scrapy
from master.items import MasterItem
import re


class StoneMasterSpider(scrapy.Spider):
    name = 'stone_master'
    allowed_domains = ['www.kingstone.com.tw']
    # start_urls = ['http://www.kingstone.com.tw/']
    start_urls = ['https://www.kingstone.com.tw/mag/mag_class.asp?actid=MainTop&class_id=dc', # 科技電腦／應用程式
        'https://www.kingstone.com.tw/mag/mag_class.asp?class_id=dd'] # 科技電腦／網路通訊
    

    def parse(self, response):
        print(response) # <200 https://www.kingstone.com.tw/mag/mag_class.asp?actid=MainTop&class_id=dc>
        # 本次採用scrapy內建的selector.HtmlXPathSelector()來解析網頁並取得網址
        # 先將預設的response轉存為hxs (HtmlXPathSelector)
        hxs = scrapy.selector.HtmlXPathSelector(response)
        # hlist = response.xpath('.//nav[@class="navcolumn_classlevel"]/ul//li/a/attribute::href').extract() # 本次不使用陽春的xpath
        # 利用hxs.select搜索並存成列表
        hlist = hxs.select('.//li/a[contains(@href,"basic")]/@href').re(r'/new/basic/([0-9]+)') # contains包含@代表屬性，"代表文字" 很方便
        for vo in hlist:
            item = MasterItem()
            item['url'] = vo
            yield item
        next_page = re.findall(r'<a href="/mag/mag_class.asp.*?class_id=(\w+).*?&page=([0-9]+).*?下一頁',response.text)
        
        # 若有搜到，則回傳一個Request，將搜到的url傳出去，並調用自己再次進行解析。直到沒有下一頁。
        if next_page:
            next_url = "https://www.kingstone.com.tw/mag/mag_class.asp?class_id="+next_page[0][0]+"&act_class=0&page="+next_page[0][1]
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
