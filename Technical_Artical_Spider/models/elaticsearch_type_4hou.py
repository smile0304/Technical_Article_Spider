from Technical_Artical_Spider.models.common import ik_analyzer
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class Article_4houType(DocType):
    suggest = Completion(analyzer=ik_analyzer)  #搜索建议
    image_local = Keyword()
    title = Text(analyzer="ik_max_word")
    url_id = Keyword()
    create_date = Date()
    url = Keyword()
    author = Keyword()
    tags = Text(analyzer="ik_max_word")
    watch_nums = Integer()
    comment_nums = Integer()
    praise_nums = Integer()
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "teachnical_article"
        doc_type = "A_4hou"


if __name__ == "__main__":
    Article_4houType.init()
