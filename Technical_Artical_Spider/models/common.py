
#据说是个bug,反正就是要这样写
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])