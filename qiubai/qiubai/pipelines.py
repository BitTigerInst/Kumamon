# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class QiubaiPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri  # 指定了mongodb的服务器
        self.mongo_db = mongo_db  # 指定了mongodb的database

    @classmethod
    def from_crawler(cls, crawler):
        # 这里通过抓取器crawler返回的是当前的类QiubaiPipeline的一个实例
        # decorator里面可以仔细研究下
        # crawler.settings指的是settings.py这个文件
        # 这里从settings.py里面获取mongo_uri和mongo_database的值
        # 用于实例化一个QiubaiPipeline机器人！
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    # 建立pymongo的连接
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 关闭pymongo连接
    def close_spider(self, spider):
        self.client.close()

    # 这里是实际的处理method
    # 这里的具体处理是把item首先变成dict，然后插入到collection中
    # 至于找到找个数据并提取出来是通过Spider类的实例spider来实现！
    def process_item(self, item, spider):
        collection_name = item.__class__.__name__  # item这个类的名字作为collection名字
        #self.db[collection_name].remove({})

        self.db[collection_name].insert(dict(item))  # 存储到mongodb中
        return item
