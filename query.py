from elasticsearch import Elasticsearch

# query: 要搜索的查询词
# field: 要搜索的特定字段
# param query_type: 查询类型（'match', 'prefix', 'wildcard', 'regexp'）
# return: 匹配结果的字典

class PaperSearch:
    def __init__(self, index_name='papers'):
        # host = "http://localhost:9200"
        self.es = Elasticsearch()
        self.index_name = index_name
        

    def _search(self, query, field=None, size=20, query_type='match' ):
        if query_type == 'prefix':
            match_part = {"prefix": {field: query}}
        elif query_type == 'wildcard':
            match_part = {"wildcard": {field: query}}
        elif query_type == 'regexp':
            match_part = {"regexp": {field: query}}
        else:
            if field:
                match_part = {"match": {field: {"query":query,"fuzziness":"AUTO"}}}
            else:
                match_part = {"multi_match": {"query": query, "fields": ["*"],"fuzziness":"AUTO"}}
# 查询test索引中，name字段为杨晨的数据
# print(es.search(index='test', query={'match_phrase':{'name':'杨晨'}}))
        # 构造请求体
        body = {
            "query": match_part,
            
            "highlight": {
                "fields": {
                    "*": {}
                }
            },
            "size" : size
            
        }


        response = self.es.search(index=self.index_name, body=body)

        results = {}
        for hit in response['hits']['hits']:
            paper_id = hit['_source'].get('paper_id')
            highlights = hit.get('highlight', {})
            results[paper_id] = highlights

        return results

    def search_all_fields(self, query, field, size, query_type='match'):
        return self._search(query, None, size=size, query_type=query_type)

    def search_specific_field(self, query, field, size, query_type='match'):
        return self._search(query, field, size=size, query_type=query_type)

# 使用示例
if __name__ == "__main__":
    paper_search = PaperSearch()

    prefix_results = paper_search.search_specific_field('rock', 'title', 10, query_type='match')
    print(prefix_results)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用前缀查询
    # prefix_results = paper_search.search_specific_field('roc', 'title', 10, query_type='prefix')
    # print(prefix_results)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用通配符查询
    # wildcard_results = paper_search.search_specific_field('roc*', 'title', 10, query_type='wildcard')
    # print(wildcard_results)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # # 使用正则表达式查询
    # regexp_results = paper_search.search_specific_field('roc.*', 'title', 10, query_type='regexp')
    # print(regexp_results)