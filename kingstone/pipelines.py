# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis


class KingstonePipeline(object):
    # 構造redis實例
    def __init__(self,host,port):
        self.r = redis.Redis(host=host,port=port,db=6)
    
    # 返回settings導入資料庫的host、port
    @classmethod
    def from_crawler(cls,crawler):
        host = crawler.settings.get("REDIS_HOST")
        port = crawler.settings.get("REDIS_PORT")
        return cls(host,port)

    def process_item(self, item, spider):
        if self.r.sadd('temp',item['url']):
            self.r.lpush('tag:books_tag',item['url'])
        else : 
            self.r.lpush('not_found',item['url'])
        return item
