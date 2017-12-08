# -*- coding: utf-8 -*-
import scrapy
import json
from Technical_Artical_Spider.items import ArticleSpideranquanke
from urllib import parse
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from Technical_Artical_Spider.settings import EXECUTABLE_PATH
import re
class Anquanke360Spider(scrapy.Spider):
    name = 'anquanke360'
    allowed_domains = ['anquanke.com']
    start_urls = ['https://api.anquanke.com/data/v1/posts?page=2&size=10&category=knowledge/']
    headers_api = {
        "HOST": "api.anquanke.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }
    headers_article = {
        "HOST": "www.anquanke.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
        super(Anquanke360Spider,self).__init__()
        dispatcher.connect(self.spider_close,signals.spider_closed)

    def spider_close(self,spider):
        self.browser.quit()


    def parse(self, response):
        article_json = json.loads(response.text)
        next_url = article_json["next"]

        for data in article_json["data"]:
            url = "https://www.anquanke.com/post/id/"+str(data["id"])
            title = data["title"]
            title_start = re.search("(^\d{1,2}月\d{1,2}日)",title)
            if not title_start:
                cover_image = data["cover"]
                item = ArticleSpideranquanke()
                item["id"] = data["id"]
                item["url"] = url
                item["title"] = title
                item["create_time"] = data["date"].split(" ")[0]
                item["image_url"] = [cover_image]
                item["watch_num"] = data["pv"]
                tags_list = data["tags"]
                item["tags"] = ",".join(tags_list)
                item["author"] = data["author"]["nickname"]
                yield scrapy.Request(url,
                               headers=self.headers_article,
                               meta={"image_url": parse.urljoin(response.url, cover_image)},
                               callback=lambda arg1=response,arg2=item: self.parse_detail(arg1,arg2))

        if next_url:
            yield scrapy.Request(next_url,headers=self.headers_api,callback=self.parse)


    def parse_detail(self,response,item):
        item["content"] = response.xpath("//div[@class='article-content']").extract()[0]
        item["comment_num"] = int(response.css(".comment::text").extract()[0])
        item['ArticlecontentImage'] = response.css(".aligncenter::attr(data-original)").extract()
        yield item
