# -*- coding: utf-8 -*-
import json

import requests
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ziroom.items import ZiroomItem, ZiroomItemLoader
from ziroom.utils.common import get_md5
from scrapy.http import Request
import re


class Ziroom_phoneSpider(CrawlSpider):
    name = 'ziroom_phone'
    allowed_domains = ['www.ziroom.com', 'm.ziroom.com','//www.ziroom.com']
    start_urls = ['http://www.ziroom.com/z/nl/z1.html?p=1']

    rules = (
        Rule(LinkExtractor(allow=r'www.ziroom.com/z/nl/z1.html.*'), callback='parse_list',follow=True),
        Rule(LinkExtractor(allow=r'z/vr/\d+..html'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'v7/room/detail.json?city_code=110000&id=\d+..html'), callback='parse_room',
             follow=False),

    )

    def parse_list(self, response):
        next_url = response.css(".next::attr(href)").extract()[0]
        print("next url:"+next_url[2:])

        yield Request(url="http://"+next_url[2:],
                      callback=self.parse_list)


    def parse_item(self, response):
        url = response.url
        match_re = re.match(r'http://www.ziroom.com/z/vr/(\d+.).html', url)

        if match_re:
            num = match_re.group(1)
        else:
            print("error url:" + url)
        yield Request(url="http://m.ziroom.com/v7/room/detail.json?city_code=110000&id=" + num,
                      callback=self.parse_room)


    def parse_room(self, response):

        print("获取地址:" + response.url)
        jsobj = json.loads(response.body)
        comment = jsobj['data']
        if comment:
            print("OK")
            pass
        else:
            print("false")
            time.sleep(20)
            return Request(url="http://www.ziroom.com",
                          callback=self.parse_item)
        print("开始解析")
        item_loader = ZiroomItemLoader(item=ZiroomItem(), response=response)
        item_loader.add_value("title", comment['resblock']['name'])
        item_loader.add_value("url", response.url)
        print("打印url"+response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("location_lable", comment['resblock']['surround'])
        item_loader.add_value("room_tags", comment['tags'])
        item_loader.add_value("area", comment['area'])
        item_loader.add_value("direction", comment['introduction'])
        item_loader.add_value("type", comment['face'])
        item_loader.add_value("floor", comment['floor'])
        item_loader.add_value("transportation", comment['resblock']['traffic'])
        item_loader.add_value("is_booking", comment['status'])
        item_loader.add_value("room_no", comment['house_code'])
        item_loader.add_value("content", comment['resblock']['around'])
        item_loader.add_value("configuration", "null")
        item_loader.add_value("room_price", comment['price'])
        item_loader.add_value("price_type", comment['price_unit'] + "," + comment['price_desc'])

        item_loader.add_value("location", str(comment['resblock']['lng']) + "," + str(comment['resblock']['lat']));
        item_loader.add_value("status", 0)
        ziRoomItem = item_loader.load_item()
        return ziRoomItem
