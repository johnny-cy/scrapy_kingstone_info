# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import re

class MasterPipeline(object):
    # 初始化用來連接Redis數據庫
    def __init__(self,host,port):
        self.r = redis.Redis(host=host,port=port,db=5)
        
    # 固定寫法，單純為了將settings.py當中的常數導入本類別使用。
    @classmethod
    def from_crawler(cls,crawler):
        host = crawler.settings.get("REDIS_HOST")
        port = crawler.settings.get("REDIS_PORT")
        return cls(host,port)

    # 處理由spiders傳過來的item
    def process_item(self, item, spider):
        if self.r.sadd('bookid',item['url']):
            url = "https://www.kingstone.com.tw/new/basic/"+item['url'] 
            self.r.lpush('ok_urls', url)
        else:
            self.r.lpush('nok_urls',item['url'])
        
        
        
        return item
