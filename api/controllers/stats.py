import requests
import json
from flask import Blueprint
from flask import jsonify
from api.lib.helper import is_up_to_date
from api.models.stats import Stats
from api.controllers.tags import get_tag
from api.models.tags import Tag
from ..models.tags import Tag
from flask import request, url_for


stats_endpoint = Blueprint('stats', __name__, url_prefix='/api/v1/stats')


@stats_endpoint.route('/question_frequency', methods=['POST'])
def get_question_frequency():
    tags_name = request.json["tags"]
    tags_name = tags_name.split(";")
    responses = [get_tag(tag=tag_name) for tag_name in tags_name]
    responses_json = [response[0] for response in responses if response[1] == 200]
    tags_as_json = [json.loads(response_json.get_data()) for response_json in responses_json]
    tags = [Tag.from_json(tag_as_json["tag"]) for tag_as_json in tags_as_json]
    if not tags:
        return jsonify(error=401), 401
    return jsonify(result=Stats.get_question_frequency(tags)), 200
