# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
import time
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
from ziroom.settings import SQL_DATETIME_FORMAT, SQL_DATETIME_FORMAT

class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
    )
    location_lable = scrapy.Field()
    room_tags = scrapy.Field()
    area = scrapy.Field()
    direction = scrapy.Field()
    type = scrapy.Field()
    floor = scrapy.Field()
    transportation = scrapy.Field()
    is_booking = scrapy.Field()
    content = scrapy.Field()
    room_no = scrapy.Field()
    configuration = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_time = scrapy.Field()
    up_load_time = scrapy.Field()
    price_type = scrapy.Field()
    room_price = scrapy.Field()
    status = scrapy.Field()

    def get_insert_sql(self):
        now_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        insert_sql = """
               insert into room(title,location_lable ,room_tags,area,direction,type,floor,transportation,is_booking,content,room_no
               ,configuration,location,url,url_object_id,create_time,up_load_time,status,room_price,price_type)
                 VALUES (%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s)
                  ON DUPLICATE KEY UPDATE room_price=VALUES(room_price), room_price=VALUES(room_price),
              create_time=VALUES(create_time)
             """
        params = (self["title"], self["location_lable"], self["room_tags"], self["area"], self["direction"], self["type"], self["floor"], self["transportation"], self["is_booking"], self["content"]
                  , self["room_no"], self["configuration"],self["location"], self["url"], self["url_object_id"], now_time, now_time, self["status"], self["room_price"], self["price_type"])
        return insert_sql,params


class ZiroomItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()
