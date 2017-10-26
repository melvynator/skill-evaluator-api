from .. import es
import datetime

QUESTION_QUERY = {
        "size": 1,
        "query": {
            "match":{
                "name": ""
            }
        }
}

GENERAL_QUERY = {
                "size": 0,
                "query": {
                    "match_all": {}
                },
                "_source": {
                    "excludes": []
                },
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "month",
                            "interval": "1y",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        }
                    }
                }
            }


class Stats:

    @staticmethod
    def get_percentage_of_jobs(technos, interval):
        general_query = GENERAL_QUERY
        general_query["aggs"]["2"]["date_histogram"]["interval"] = interval
        general_query_response = es.search(index="jobs", doc_type="ycombinator", body=general_query)
        general_query_buckets = general_query_response["aggregations"]["2"]["buckets"]
        buckets = [bucket["key_as_string"] for bucket in general_query_buckets]
        general_query_dict = {bucket["key_as_string"]: bucket["doc_count"] for bucket in general_query_buckets}
        queries = [{"size": 0, "query": {"match": {"post": techno}},
                "aggs": {techno: {"date_histogram": {"field": "month", "interval": interval}}}} for techno in technos]
        combined_aggregation = {}
        for query in queries:
            response = es.search(index="jobs", doc_type="ycombinator", body=query)
            techno_name = list(response["aggregations"].keys())[0]
            combined_aggregation[techno_name] = {bucket["key_as_string"]:bucket["doc_count"]
                                                 for bucket in response["aggregations"][techno_name]["buckets"]}
        result = {"buckets":buckets, "values": {}}
        for techno, frequency in combined_aggregation.items():
            result["values"][techno] = [(frequency[bucket]*100.0)/general_query_dict[bucket] if bucket in frequency
                                       else 0 for bucket in buckets]
        return result

    @staticmethod
    def get_question_frequency(tags):
        queries = [{'size': 1, 'query': {'match': {'name': tag.name}}} for tag in tags]
        responses = list(map(lambda query: es.search(index="stackoverflow", doc_type="tag", body=query), queries))
        question_per_techno = [(response["hits"]["hits"][0]["_source"]["question_frequency"],
                                response["hits"]["hits"][0]["_source"]["name"]) for response in responses]
        timestamps = sorted(list({int(item["from"]) for techno in question_per_techno for item in techno[0]}))
        buckets = list(map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).strftime("%B %Y"), timestamps))
        result = {"buckets": buckets, "values": {}}
        for techno in question_per_techno:
            result["values"][techno[1]] = [item["count"] if int(item["from"]) in timestamps else 0 for item in techno[0]]
        print(result)
        return result


