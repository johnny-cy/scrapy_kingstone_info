# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import re
import json

class SlavePipeline(object):
    def __init__(self,host,port):
        self.r = redis.Redis(host=host,port=port,db=6)
       
    @classmethod
    def from_crawler(cls,crawler):
        host = crawler.settings.get("REDIS_HOST")
        port = crawler.settings.get("REDIS_PORT")
        return cls(host,port)

    def process_item(self, item, spider):
        adict = {}
        for k,v in item.items():
            adict[k] = v
            a = json.dumps(adict)
            self.r.lpush('save_books:items',a)
            
        return item
