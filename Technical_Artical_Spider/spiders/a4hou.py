# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from Technical_Artical_Spider.items import ArticleSpider4hou,ArticleItemLoader
from Technical_Artical_Spider.utils.common import get_md5
class A4houSpider(scrapy.Spider):
    name = '4hou'
    allowed_domains = ['www.4hou.com']
    start_urls = ['http://www.4hou.com/page/1']
    #start_urls = ['http://www.4hou.com/vulnerable/8663.html']
    headers = {
        "HOST": "www.4hou.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
    }
    urls = {}

    def parse(self, response):
        #提取出下一页的url
        next_url = response.css(".post-read-more-new a::attr(href)").extract()[0]
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url,next_url),headers=self.headers,callback=self.parse)

        #提取出页面中全部的URL
        Article_Boxs  = response.css(".main-box .ehover1")
        for Article_box in Article_Boxs:
            Article_url = Article_box.css(".new_img_title::attr(href)").extract_first("")
            #过滤出技术文章，不要新闻
            match_obj = re.match("(.*4hou.com/(technology|reverse|penetration|web|vulnerable)/(\d+)\.html$)", Article_url)
            if match_obj:
                Image_url = Article_box.css(".new_img .wp-post-image::attr(data-original)").extract_first("")
                yield scrapy.Request(url = parse.urljoin(response.url,Article_url),
                                     headers=self.headers
                                     ,meta={"image_url":parse.urljoin(response.url,Image_url)}
                                     ,callback=self.parse_detail)

    def parse_detail(self,response):
        image_url = response.meta.get("image_url","") #文章封面图
        item_loader =ArticleItemLoader(item=ArticleSpider4hou(),response=response)
        item_loader.add_css("title",".art_title::text")
        item_loader.add_css("create_date",".art_time::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_id",get_md5(response.url))
        item_loader.add_css("author",".article_author_name .upload-img::text")
        item_loader.add_xpath('tags',"//*[@class='art_nav']/a[2]/text()")
        item_loader.add_value('image_url',[image_url])
        item_loader.add_css("watch_num",".newtype .read span::text")
        item_loader.add_css("comment_num",".newtype .comment span::text")
        item_loader.add_css("praise_nums",".newtype .Praise span::text")
        item_loader.add_css("content",".article_cen")
        #文章中引用的图片
        item_loader.add_css("ArticlecontentImage",".article_cen img::attr(data-original)")
        article_item = item_loader.load_item()
        yield article_item
