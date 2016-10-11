# -*- coding: utf-8 -*-
import scrapy
from video.items import VideoItem

class HentaiSpider(scrapy.Spider):
    name = "hentai"
    allowed_domains = ["madthumbs.com"]
    start_urls = (
        'http://m.madthumbs.com/hentai',
    )

    custom_settings = {
                'FILES_STORE' : '/home/cui/视频/hentai'
            }

    def parse(self, response):
        item = VideoItem()
        item['file_urls'] = response.xpath("//a[contains(@href,'http://mobile.madthumbscdn.com/videos')]/@href").extract()
        yield item
        next_url = response.xpath('//a[@data-iconpos="right"]/@href').extract()
        if next_url:
            yield scrapy.Request(next_url[0] , self.parse)
