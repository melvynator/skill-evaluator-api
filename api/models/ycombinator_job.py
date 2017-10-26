from .. import es
import hashlib
import datetime


class YcombinatorJob:

    def __init__(self):
        self.poster = ""
        self.month = datetime.date(year=1912, month=6, day=23)
        self.post = ""

    @classmethod
    def from_crawler(cls, poster, post, month):
        obj = cls()
        obj.poster = poster
        obj.post = post
        obj.month = month
        return obj

    def save_to_es(self):
        data = self.to_json()
        job_id = hashlib.sha224((str(self.month) + self.post).encode('utf-8')).hexdigest()
        print(job_id)
        es.index(id=job_id, index="jobs", doc_type="ycombinator", body=data)

    def to_json(self):
        return dict(month=str(self.month), poster=self.poster, post=self.post)

    def __str__(self):
        return str(self.month) + ": " + str(self.poster)

    def __repr__(self):
        return str(self.month) + ": " + str(self.poster)
