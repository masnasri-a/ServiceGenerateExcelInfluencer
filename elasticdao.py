from elasticsearch import Elasticsearch

class elastic_dao:
    def get_data_elastic(influencer,start,end):
        es = Elasticsearch(hosts='locahhost:9200')
        bodies = {"query": {"bool": {"must": [
            {"nested": {"path": "ann_statements",
                        "query": {"match_phrase": {"ann_statements.influencer": influencer}}}},
            {"range": {"created_at": {"gte": start, "lte": end, "format": "yyyyMMdd", "time_zone": "Asia/Jakarta"}}}]}},
            "_source": ["source", "ann_statements", "title"], "sort": [{"created_at": {"order": "desc"}}]}
        response = es.search(index='ima-online-news-hot-*', doc_type='_doc', body=bodies)
        hits = response['hits']['hits']
        num = 0
        data_list = []
        for hit in hits:
            source = hit['_source']
            for statement in source['ann_statements']:
                if "influencer" in statement:
                    statement_influencers = statement['influencer']
                    if statement_influencers == influencer:
                        lists = []
                        lists.append(statement['created_at'])
                        lists.append(influencer.capitalize())
                        lists.append(statement['opinion'])
                        lists.append(source['title'])
                        lists.append(source['source'])
                        num += 1
                        data_list.append(lists)
        return data_list,num