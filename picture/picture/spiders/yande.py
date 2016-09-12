# -*- coding: utf-8 -*-
import scrapy
from picture.items import PictureItem


class YandeSpider(scrapy.Spider):
    name = "yande"
    allowed_domains = ["yande.re"]
    start_urls = (
        'https://yande.re/post?tags=rating:e&page=1',
    )

    custom_settings = {
                'FILES_STORE' : '/home/cui/图片/yande'
            }

    def parse(self, response):
        item = PictureItem()
        item['file_urls'] = response.css("a.directlink.largeimg::attr('href')").extract()
        yield item
        next_url = response.css("a.next_page::attr('href')").extract()
        if next_url:
            next_url = response.urljoin(next_url[0])
            yield scrapy.Request(next_url , self.parse)
