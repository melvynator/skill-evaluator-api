import json
import datetime
from api.lib.stackoverflow_helper import add_months


def create_index(es, index_name, mapping_name):
    print("Load mappig")
    with open("../data/{0}.json".format(mapping_name)) as mapping_file:
        mapping = json.load(mapping_file)

    print("Create index")
    if not es.indices.exists(index_name):
        es.indices.create(index=index_name, body=mapping)


def is_up_to_date(tag):
    if not tag.last_update:
        return False
    if add_months(datetime.datetime.fromtimestamp(int(tag.last_update)), 1) >= datetime.date.today():
        return True
    else:
        return False