# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# class Bqg2Pipeline(object):
#     def process_item(self, item, spider):
#         return item
class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
                   database=crawler.settings.get('MYSQL_DATABASE'),
                   user=crawler.settings.get('MYSQL_USER'),
                   password=crawler.settings.get('MYSQL_PASSWORD'),
                   port=crawler.settings.get('MYSQL_PORT'),
                   )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['% s'] * len(data))
        sql = 'insert into downloadtxt (% s) values (% s)' % ( keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

