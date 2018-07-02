# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import  sys
import  os
import re
#获取绝对路径的 父目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy","crawl","ziroom_phone"])
execute(["scrapy","crawl","ziroom"])

