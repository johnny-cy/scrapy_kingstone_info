# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SlaveItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field() # id
    title = scrapy.Field() # 書名
    catagory = scrapy.Field() # 類別
    publish_date = scrapy.Field() # 出版日期
    price = scrapy.Field() # 價格
    img = scrapy.Field() # 圖片
    language = scrapy.Field() # 語言
    context = scrapy.Field() # 內容簡介
    contents = scrapy.Field() # 章節目錄
    author = scrapy.Field() # 作者
    editorreco = scrapy.Field() # 編輯推薦
