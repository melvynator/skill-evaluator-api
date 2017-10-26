from flask import Blueprint
from flask import jsonify
from flask import request
from ..models.stats import Stats

jobs_endpoint = Blueprint('jobs', __name__, url_prefix='/api/v1/jobs')


@jobs_endpoint.route('/', methods=['POST'])
def is_present():
    data = request.get_json()
    keywords = data.get('techno')
    techno = keywords.split(";")
    interval = data.get('interval')
    result = Stats.get_percentage_of_jobs(techno, interval)
    return jsonify(result=result), 200
