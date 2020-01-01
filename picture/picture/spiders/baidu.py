# -*- coding: utf-8 -*-
import os

import scrapy
from picture.items import PictureItem
from scrapy.utils.project import get_project_settings


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    pn = 0
    target = "仓木麻衣"
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&word=' + target
    custom_settings = {
        'IMAGES_STORE': os.path.join(get_project_settings().get('IMAGES_STORE'), name, target)
    }

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        item = PictureItem()
        item['image_urls'] = response.selector.re(r'''"objURL":"(http://[^"]+?)"''')
        yield item
        self.pn += 60
        yield scrapy.Request('%s%s%d' % (self.url, '&pn=', self.pn), self.parse)
