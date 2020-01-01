# -*- coding: utf-8 -*-
import os

import scrapy
from picture.items import PictureItem
from scrapy.utils.project import get_project_settings


class JandanSpider(scrapy.Spider):
    name = 'jandan'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx']
    custom_settings = {
        'IMAGES_STORE': os.path.join(get_project_settings().get('IMAGES_STORE'), name)
    }

    def parse(self, response):
        item = PictureItem()
        image_urls = response.xpath("//a[@class='view_img_link']/@href").extract()
        item['image_urls'] = ['http:' + url for url in image_urls]
        yield item
        next_url = response.xpath("//a[@class='previous-comment-page']/@href").extract()
        if next_url:
            yield scrapy.Request('http:' + next_url[0], self.parse)
