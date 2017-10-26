import requests
from elasticsearch import Elasticsearch
from api.lib.helper import create_index
from api.models.tags import Tag

BASE_URL = "https://api.stackexchange.com/2.2/tags?page={0}&pagesize=100&order=desc&sort=popular&site=stackoverflow&key=wH4Yhv0yV3gKdsZYY7IeCg(("

es_host = {"host": "localhost", "port": 9200}
es = Elasticsearch([es_host])
create_index(es)

page = 351
response = requests.get(BASE_URL.format(page))
response_json = response.json()
while response_json["has_more"]:
    print(page)
    response = requests.get(BASE_URL.format(page))
    response_json = response.json()
    for item in response_json["items"]:
        tag = Tag.from_api_call(item)
        tag.save_to_es()
    page += 1
