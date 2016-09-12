# -*- coding: utf-8 -*-
import scrapy
from picture.items import PictureItem

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    pn = 0
    custom_settings = {
                'FILES_STORE' : '/home/cui/图片/baidu'
            }

    def __init__(self , keywords = '' , *args , **kwargs):
        super(BaiduSpider , self).__init__(*args , **kwargs)
        self.url = 'http://image.baidu.com/search/flip?tn=baiduimage&word=' + keywords
        self.start_urls = [
                    self.url
                ]

    def parse(self, response):
        item = PictureItem()
        item['file_urls'] = response.selector.re(r'''"objURL":"(http://[^"]+?)"''')
        yield item
        self.pn += 60
        yield scrapy.Request('%s%s%d' % (self.url , '&pn=' , self.pn) , self.parse)
