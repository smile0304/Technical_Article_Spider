from Technical_Artical_Spider.models.common import ik_analyzer
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class Article_anquankeType(DocType):
    suggest = Completion(analyzer=ik_analyzer)  #搜索建议
    id = Integer()
    url = Keyword()
    title = Text(analyzer="ik_max_word")
    create_time = Date()
    cover_local = Keyword()
    watch_num = Integer()
    comment_num = Integer()
    tags = Text(analyzer="ik_max_word")
    author = Keyword()
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "teachnical_article"
        doc_type = "anquanke"


if __name__ == "__main__":
    Article_anquankeType.init()
