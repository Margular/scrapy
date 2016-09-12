# -*- coding: utf-8 -*-
import scrapy
from picture.items import PictureItem

class JandanSpider(scrapy.Spider):
    name = 'jandan'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx']

    custom_settings = {
                'FILES_STORE' : '/home/cui/图片/jandan'
            }


    def parse(self , response):
        item = PictureItem()
        item['file_urls'] = response.xpath("//a[@class='view_img_link']/@href").extract()
        yield item
        next_url = response.xpath("//a[@class='previous-comment-page']/@href").extract()
        if next_url:
            yield scrapy.Request(next_url[0] , self.parse)
