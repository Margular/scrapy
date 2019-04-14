# -*- coding: utf-8 -*-
import os
import time
import urllib.parse
import scrapy
from video.items import VideoItem
from scrapy.utils.project import get_project_settings


class PornhubSpider(scrapy.Spider):
    name = "pornhub"
    allowed_domains = ["pornhub.com", "phncdn.com"]
    target = 'tentacle+hentai'
    start_urls = (
        'https://www.pornhub.com/video/search?search=' + target,
    )
    videos = '//ul[@id="videoSearchResult"]/li/div/div/div[contains(@class, "img")]/a/@href'
    next_page = '/html/body/div[11]/div/div[6]/div[4]/ul/li[8]/a/@href'

    custom_settings = {
        'FILES_STORE': os.path.join(get_project_settings().get('FILES_STORE'), name, target),
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 30
    }


    def parse(self, response):
        links = response.xpath(self.videos).extract()
        if len(links) == 0:
            self.logger.warn("seems banned by pornhub, retry...")
            time.sleep(120)
            yield scrapy.Request(response.url, self.parse, dont_filter=True)
            return

        self.logger.debug("get links: " + repr(links))
        for link in links:
            yield response.follow(link, self.parseLink, priority=10)

        next_url = response.xpath(self.next_page).extract()[0]
        if next_url:
            yield response.follow(next_url, self.parse)

    def parseLink(self, response):
        item = VideoItem()
        try:
            video_url = response.selector.re(r'"videoUrl":"([^"]+?)"')[0].replace("\\/", "/")
        except IndexError as e:
            self.logger.warn("seems we have been detected by pornhub, retry...")
            time.sleep(120)
            yield scrapy.Request(response.url, self.parseLink, dont_filter=True, priority=100)
            return

        item['file_urls'] = [video_url]
        yield item
