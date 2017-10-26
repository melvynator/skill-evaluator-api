from flask import Blueprint
from flask import jsonify
from api.lib.helper import is_up_to_date
from api.models.stats import Stats
from ..models.tags import Tag
from flask import request


tags_endpoint = Blueprint('tags', __name__, url_prefix='/api/v1/tags')


@tags_endpoint.route('/<string:tag>', methods=['GET'])
def get_tag(tag):
    tag = Tag.get_tag_from_es(tag.strip())
    if not tag:
        return jsonify(error=401), 401
    if not is_up_to_date(tag):
        tag.set_popularity()
        tag.update_popularity()
        tag = Tag.get_tag_from_es(tag.name)
    return jsonify(tag=tag.to_json()), 200

