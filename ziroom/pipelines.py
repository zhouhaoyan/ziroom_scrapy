# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ZiroomPipeline(object):
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print("开启异常处理流程___________________________________________________________________________")
        print(failure)
        params = (failure, item["url"])
        self.dbpool.runInteraction(self.do_insert_error, params)
        print("开启异常处理结束___________________________________________________________________________")

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print ("开启异步插入:"+insert_sql, params)
        cursor.execute(insert_sql, params)

    def do_insert_error(self, cursor, params):
        # 执行error的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        print("错误信息记录:")
        insert_sql = """
               insert into error(url, error)
               VALUES (%s, %s)
           """
        cursor.execute(insert_sql, params)