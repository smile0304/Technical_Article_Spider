# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join,Identity
from Technical_Artical_Spider.models.elaticsearch_type_4hou import Article_4houType
from Technical_Artical_Spider.models.elaticsearch_type_anquanke import Article_anquankeType
from elasticsearch_dsl.connections import connections
es_4hou = connections.create_connection(Article_4houType._doc_type.using)
es_anquanke = connections.create_connection(Article_anquankeType._doc_type.using)
import scrapy

def gen_suggests(es,index,info_tuple):
    #根据字符串生生搜索建议数据
    used_words = set() #供去重使用
    suggests = []
    for text,weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index,analyzer="ik_max_word",params={'filter':["lowercase"]},body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})

    return suggests


class TechnicalArticalSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


def splitspace(value):
    value = value.strip()
    value = value.replace('\n','')
    value = value.replace('\r','')
    return value

def remove_comma(value):
    if "," in value:
        return value.replace(",","")
    else:
        return value

def remove_Keywords(value):
    if "发布" in value:
        value = value.replace("发布", "")
    if "前" in value:
        #now_time = time.strftime("%Y-%m-%d")
        import time
        now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        return now_time
    else:
        time = value.replace("年","-").replace("月","-").replace("日","")
        return time

def return_value(value):
    return value

def return_intvalue(value):
    value =  int(value)
    return value

def seturl(value):
    if value == None:
        return value
    elif value.startswith("http://") or value.startswith("https://"):
        return value
    else:
        return "http://www.4hou.com"+value

#嘶吼文章Item
class ArticleSpider4hou(scrapy.Item):
    image_local = scrapy.Field() #图片本地地址
    image_url =scrapy.Field(
        output_processor=MapCompose(return_value)
    ) #图片地址
    title = scrapy.Field()  #文章标题
    create_date = scrapy.Field(
        input_processor=MapCompose(remove_Keywords),
    ) #发布日期
    url = scrapy.Field()  #原文地址
    url_id = scrapy.Field() #经过md5加密过后的url  作为主键
    author = scrapy.Field(
        input_processor =MapCompose(splitspace),
    ) #作者
    tags = scrapy.Field() #标签
    watch_num = scrapy.Field(
        input_processor=MapCompose(remove_comma,return_intvalue),
    ) #观看数量
    comment_num = scrapy.Field(
        input_processor=MapCompose(remove_comma,return_intvalue),
    ) #评论数量
    praise_nums =scrapy.Field(
        input_processor=MapCompose(remove_comma,return_intvalue),
    ) #点赞数量
    content = scrapy.Field() #文章正文
    #文章中的背景图处理
    ArticlecontentImage = scrapy.Field(
        input_processor = MapCompose(seturl),
        output_processor = Identity(),

    )

    # TODO 评论信息的显示
    def get_insert_sql(self):
        insert_sql = """
            insert into 4hou_Article(
            image_local,
            title,
            url_id,
            create_date,
            url,
            author,
            tags,
            watch_num,
            comment_num,
            praise_nums,
            content
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE watch_num=VALUES(watch_num),
            comment_num=VALUES(comment_num),praise_nums=VALUES(praise_nums)
        """
        params= (
              self["image_url"],
              self["title"],
              self["url_id"],
              self["create_date"],
              self["url"],
              self["author"],
              self["tags"],
              self["watch_num"],
              self["comment_num"],
              self["praise_nums"],
              self["content"]
                  )
        return insert_sql,params
    ##将数据写入es
    def save_to_es(self):
        article = Article_4houType()
        article.image_local = self["image_url"]
        article.title = self["title"]
        article.url_id = self["url_id"]
        article.create_date = self["create_date"]
        article.url = self["url"]
        article.author = self["author"]
        article.tags = self["tags"]
        article.watch_nums = self["watch_num"]
        article.comment_nums = self["comment_num"]
        article.praise_nums = self["praise_nums"]
        article.content = self["content"]
        article.suggest = gen_suggests(es_4hou,Article_4houType._doc_type.index,((article.title,10),(article.tags,7)))
        article.save()

        return

#安全客文章Iten
class ArticleSpideranquanke(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    create_time= scrapy.Field()
    image_url = scrapy.Field()
    image_local = scrapy.Field()
    watch_num = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    comment_num = scrapy.Field()
    content = scrapy.Field()
    ArticlecontentImage = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into anquanke_article(
            id,
            url,
            title,
            create_time,
            cover_local,
            watch_num,
            tags,
            author,
            comment_num,
            content
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE watch_num=VALUES(watch_num),
            comment_num=VALUES(comment_num)
        """
        params = (
            self["id"],
            self["url"],
            self["title"],
            self["create_time"],
            self["image_url"],
            self["watch_num"],
            self["tags"],
            self["author"],
            self["comment_num"],
            self["content"]
        )
        return insert_sql, params
    #将代码写入es
    def save_to_es(self):
        article = Article_anquankeType()
        article.id = self["id"]
        article.url = self["url"]
        article.title = self["title"]
        article.create_time = self["create_time"]
        article.cover_local = self["image_url"]
        article.watch_num = self["watch_num"]
        article.tags = self["tags"]
        article.author = self["author"]
        article.comment_num = self["comment_num"]
        article.content = self["content"]
        article.suggest = gen_suggests(es_anquanke,Article_anquankeType._doc_type.index,((article.title,10),(article.tags,7)))
        article.save()

        return