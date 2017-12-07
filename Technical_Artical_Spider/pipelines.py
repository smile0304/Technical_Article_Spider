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


class ArticleImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        content_image = request.url.split('/')[-1]
        return 'Cover_images/%s' % (content_image)

    def item_completed(self, results, item, info):
        if "image_url" in item:
            for ok,value in results:
                image_file_path = value["path"]
            item["image_local"] = image_file_path
        return item

class ArticlecontentImagePipline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        content_image = request.url.split('/')[-1]
        return 'Content_images/%s' % (content_image)

    def get_media_requests(self, item, info):
        if len(item["ArticlecontentImage"]):
            for image_content_url in item["ArticlecontentImage"]:
                print(image_content_url)
                yield scrapy.Request(image_content_url)

    def item_completed(self, results, item, info):
        return_list = []
        if "ArticlecontentImage" in item:
            for ok,value in results:
                image_content_path = value["path"]
                return_list.append(image_content_path)
            item["ArticlecontentImage"] = return_list
        return item


class ArticleHTMLreplacePipline(object):
    # exchange html <img>
    def process_item(self,item,spider):
        if "content" not in item:
            return item
        content = item["content"]
        sum = len(re.findall('<p style="text-align.*<img.*[<\/noscript>$]',content))
        if sum != len(item["ArticlecontentImage"]):
            return item
        if item["ArticlecontentImage"]:
            for exf in range(sum):
                html = item["ArticlecontentImage"][exf]
                html = '<center><p><img src="../images/{0}" /></p></center>'.format(html)
                content = re.sub('<p style="text-align.*<img.*[<\/noscript>$]',html,content,1)

        item["content"] = content
        return item

