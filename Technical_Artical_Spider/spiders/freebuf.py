# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from Technical_Artical_Spider.items import ArticleItemLoader,ArticleSpiderfreebuf
from Technical_Artical_Spider.utils.common import get_md5
class FreebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = ['www.freebuf.com']
    start_urls = ['http://www.freebuf.com/vuls',
                  'http://www.freebuf.com/sectool',
                  'http://www.freebuf.com/articles/web',
                  'http://www.freebuf.com/articles/system',
                  'http://www.freebuf.com/articles/network',
                  'http://www.freebuf.com/articles/wireless',
                  'http://www.freebuf.com/articles/terminal',
                  'http://www.freebuf.com/articles/database',
                  'http://www.freebuf.com/articles/security-management',
                  'http://www.freebuf.com/articles/es',
                  'http://www.freebuf.com/ics-articles'
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        next_url = response.css(".news-more a::attr(href)").extract()[0]
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

        Article_Boxs = response.css(".news-detial .news_inner")
        for article in Article_Boxs:
            Image_url = article.css(".news-img img::attr(src)").extract()[0].split('!')[0]
            Article_url = article.css(".news-info a::attr(href)").extract()[0]
            yield  scrapy.Request(url=parse.urljoin(response.url,Article_url),
                                  meta={"image_url": parse.urljoin(response.url,Image_url)},
                                  callback=self.parse_detail
                                  )

    def parse_detail(self,response):
        image_url = response.meta.get("image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=ArticleSpiderfreebuf(), response=response)
        item_loader.add_css("title",".articlecontent .title h2::text")
        item_loader.add_css("author",".property .name a::text")
        item_loader.add_css("create_date",".property .time::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_id",get_md5(response.url))
        item_loader.add_css("tags",".property .tags a::text")
        item_loader.add_value("image_url",[image_url])
        item_loader.add_css("watch_num",".property .look strong::text")
        if len(response.css(".main-tit02 h3 span::text").extract()) != 0:
            item_loader.add_css("comment_num",".main-tit02 h3 span::text")
        else:
            item_loader.add_value("comment_num","0")
        item_loader.add_css("content","#contenttxt")
        article_item = item_loader.load_item()
        yield article_item

