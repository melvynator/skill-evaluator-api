from .. import POPULARITY_URL
from .. import es
from .. import STACKOVERFLOW_INITIAL_DATE
from ..lib.stackoverflow_helper import add_months
import hashlib
import datetime
import requests


class Tag:

    def __init__(self):
        self.name = ""
        self.count = -1
        self.last_update = datetime.date(year=1912, month=6, day=23)
        self.popularity = []
        self.last_update = ""

    @classmethod
    def from_api_call(cls, json_value):
        obj = cls()
        obj.name = json_value["name"]
        obj.count = json_value["count"]
        return obj

    @classmethod
    def from_json(cls, json_value):
        obj = cls()
        if "name" in json_value:
            obj.name = json_value["name"]
        if "count" in json_value:
            obj.count = json_value["count"]
        if "question_frequency" in json_value:
            obj.popularity = json_value["question_frequency"]
        if "last_update" in json_value:
            obj.last_update = json_value["last_update"]
        return obj

    @classmethod
    def get_tag_from_es(cls, tag_name):
        obj = cls()
        tag_id = hashlib.sha224(tag_name.encode('utf-8')).hexdigest()
        data = es.get(ignore=404, index="stackoverflow", doc_type="tag", id=tag_id)
        if data["found"]:
            obj.name = data["_source"]["name"]
            obj.count = data["_source"]["count"]
            if "question_frequency" in data["_source"]:
                obj.popularity = data["_source"]["question_frequency"]
            if "last_update" in data["_source"]:
                obj.last_update = data["_source"]["last_update"]
            return obj
        else:
            return None

    def save_to_es(self):
        data = {
                 "name": self.name,
                 "count": self.count,
                 "last_update": datetime.date.today().strftime("%s")
            }
        tag_id = hashlib.sha224(self.name.encode('utf-8')).hexdigest()
        es.index(id=tag_id, index="stackoverflow", doc_type="tag", body=data)

    def update_popularity(self):
        tag_id = hashlib.sha224(self.name.encode('utf-8')).hexdigest()
        es.update(index='stackoverflow',
                  doc_type='tag',
                  id=tag_id,
                  body={"doc": {
                      "question_frequency": self.popularity,
                      "last_update": datetime.date.today().strftime("%s")
                  }})

    def set_popularity(self):
        today = datetime.date.today()
        cursor = STACKOVERFLOW_INITIAL_DATE
        popularity = []
        while cursor < today:
            begining_timestamp = cursor.strftime("%s")
            cursor = add_months(cursor, 6)
            ending_timestamp = cursor.strftime("%s")
            response = requests.get(POPULARITY_URL.format(begining_timestamp, ending_timestamp, self.name))
            response_json = response.json()
            result = {"from": begining_timestamp, "to": ending_timestamp, "count": response_json["total"]}
            popularity.append(result)
        self.popularity = popularity

    def to_json(self):
        if self.popularity:
            return dict(name=self.name, count=self.count, question_frequency=self.popularity, last_update=self.last_update)
        else:
            return dict(name=self.name, count=self.count)

    def __str__(self):
        return self.name + ": " + str(self.count)
