# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
import scrapy
import re
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from Technical_Artical_Spider.items import ArticleSpideranquanke,ArticleSpider4hou

class TechnicalArticalSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

#使用twised异步机制插入数据库
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)
    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


#将数据写入elsticsearch
class ElasticsearchPipline(object):
    #将数据写入到es中,
    def process_item(self,item,spider):
        #提升代码性能
        item.save_to_es()
        return item

class ImagesavepathPipline(ImagesPipeline):
    path = "image"

    def file_path(self, request, response=None, info=None):
        image = request.url.split('/')[-1]
        path = self.path
        return '%s/%s' % (path,image)

#文章封面图处理
class ArticleImagePipeline(ImagesavepathPipline):
    Cover_image = "image_url"

    def get_media_requests(self, item, info):
        if isinstance(item,ArticleSpideranquanke):
            self.path = "Cover_images_anquanke"
        elif isinstance(item,ArticleSpider4hou):
            self.path = "Cover_images_4hou"
        if len(item[self.Cover_image]):
            if isinstance(item,ArticleSpider4hou):
                for image_content_url in item[self.Cover_image]:
                    yield scrapy.Request(image_content_url.split("?")[0])
            else:
                for image_content_url in item[self.Cover_image]:
                    yield scrapy.Request(image_content_url)

    def item_completed(self, results, item, info):
        if self.Cover_image in item:
            for ok, value in results:
                image_file_path = value["path"]
            item[self.Cover_image] = image_file_path
        return item

#下载文章图片
class ArticlecontentImagePipline(ImagesavepathPipline):
    contentImage = "ArticlecontentImage"
    def get_media_requests(self, item, info):
        if isinstance(item,ArticleSpideranquanke):
            self.path = "Content_images_anquanke"
        elif isinstance(item,ArticleSpider4hou):
            self.path = "Content_images_4hou"
        if len(item[self.contentImage]):
            for image_content_url in item[self.contentImage]:
                yield scrapy.Request(image_content_url)

    def item_completed(self, results, item, info):
        return_list = []
        if self.contentImage in item:
            for ok,value in results:
                image_content_path = value["path"]
                return_list.append(image_content_path)
            item[self.contentImage] = return_list
        return item
#处理文章中图片的替换
class ArticleHTMLreplacePipline(object):
    # exchange html <img>
    def process_item(self,item,spider):
        if spider.name == "4hou":
            itemcontentname = "content"
            re_findall = '<p style="text-align.*<img.*[<\/noscript>$]'
            re_sub = '<p style="text-align.*<img.*[<\/noscript>$]'
            re_replace = '<center><p><img src="../images/{0}" /></p></center>'
            contentImage = "ArticlecontentImage"
        elif spider.name=="anquanke360":
            itemcontentname = "content"
            re_findall = '<img.*\.[png|jpg|gif|jpeg].*>'
            re_sub = '<img class=.*\.[png|jpg|gif|jpeg].*>'
            re_replace = '<center><p><img src="../images/{0}" /></p></center>'
            contentImage = "ArticlecontentImage"
        if itemcontentname not in item:
            return item
        content = item[itemcontentname]
        sum = len(re.findall(re_findall,content))
        if sum != len(item[contentImage]):
            return item
        if item[contentImage]:
            for exf in range(sum):
                html = item[contentImage][exf]
                html = re_replace.format(html)
                content = re.sub(re_sub,html,content,1)

        item["content"] = content

        return item