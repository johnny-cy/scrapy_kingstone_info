# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from slave.items import SlaveItem
import re
import redis

# 分布式採用scrapy_redis框架，需繼承框架底下的RedisSpider
class StoneSalveSpider(RedisSpider):
    name = 'stone_salve'
    allowed_domains = ['www.kingstone.com.tw']
    # start_urls = ['http://www.kingstone.com.tw/']
    
    # redis_key是預設好的常數，指向redis裡的資料表名稱，爬蟲時會從此隊列中獲取一條條完整的url
    redis_key = 'ok_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StoneSalveSpider, self).__init__(*args, **kwargs)
        self.r = redis.Redis(host="localhost",port=6379, db=6, decode_responses=True)
    
    def parse(self, response):
        try:
            item = SlaveItem()
            # 先將預設的response轉存為hxs (HtmlXPathSelector)
            hxs = scrapy.selector.HtmlXPathSelector(response)
            item['catagory'] = hxs.select('.//meta[@property="og:type"]/@content').extract()[0]
            item['title'] = hxs.select('.//meta[@name="keywords"]/@content').extract()[0]
            item['publish_date'] = re.search(r'<span class="title_basic">出版日：</span>(.*?)\r',response.text).group(1)
            item['price'] = re.search(r'<span class="title_basic">定價：</span><b>(.*?)</b>',response.text).group(1) 
            item['img'] = hxs.select('.//div[@class="swiper-wrapper"]//a[contains(@href,"jpg")]/@href').extract() # 回傳一個列表，因為可能是多張
            item['language'] = re.search(r'<li class="table_th">語言</li>.*?<li class="table_td">(.*?)</li>',response.text,re.S)[1]
            item['context'] = hxs.select('.//div[@id="pdintroid"]//div[@class="pdintro_txt1field"]/span').extract()[0] # 內容簡介
            # item['contents'] = hxs.select('.//div[@id="catalogid"]//div[@class="catalogfield"]/span').extract()[0] # 章節目錄
            # item['author'] = hxs.select('.//div[@id="authorintroid"]//div[@class="authorintrofield"]/span').extract()[0] # 作者
            # item['editorreco'] = hxs.select('.//div[@id="editorrecoid"]//div[@class="editorrecofield"]/span').extract()[0] # 編輯推薦
            return item
        except Exception as err:
            # 將解析錯誤的url存到一個地方
            self.r.lpush('books:failed',response.url)
