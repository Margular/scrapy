# -*- coding: utf-8 -*-
import os

import scrapy
from picture.items import PictureItem
from scrapy.utils.project import get_project_settings


class YandeSpider(scrapy.Spider):
    name = "yande"
    allowed_domains = ["yande.re"]
    start_urls = (
        'https://yande.re/post?tags=rating:e&page=1',
    )
    custom_settings = {
        'IMAGES_STORE': os.path.join(get_project_settings().get('IMAGES_STORE'), name),
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5
    }

    def parse(self, response):
        item = PictureItem()
        item['image_urls'] = response.css("a.directlink.largeimg::attr('href')").extract()
        yield item
        next_url = response.css("a.next_page::attr('href')").extract()
        if next_url:
            next_url = response.urljoin(next_url[0])
            yield scrapy.Request(next_url, self.parse)
