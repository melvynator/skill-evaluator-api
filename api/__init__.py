# Import datetime
import datetime

# Import flask and template operators
from flask import Flask, render_template

# Import elasticsearch
from elasticsearch import Elasticsearch

# Define elasticsearch
es_host = {"host": "localhost", "port": 9200}
es = Elasticsearch([es_host])

# Stackoverflow initial date
STACKOVERFLOW_INITIAL_DATE = datetime.date(year=2008, month=6, day=1)

# URLs
POPULARITY_URL = "https://api.stackexchange.com/2.2/questions?fromdate={0}&todate={1}&tagged={2}&site=stackoverflow&filter=!--KJ7DG6tXUG&key=wH4Yhv0yV3gKdsZYY7IeCg(("
YCOMBINATOR = "https://news.ycombinator.com/"
WHOISHIRING_SEED = "submitted?id=whoishiring"

# Headers
HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Import a module / component using its blueprint handler variable (mod_auth)
from api.controllers.tags import tags_endpoint
from api.controllers.jobs import jobs_endpoint
from api.controllers.stats import stats_endpoint

# from theSwitchAPI.controllers.accounts.authentification import authentication_endpoint

# Sample HTTP error handling
@app.errorhandler(404)
def not_found():
    return render_template('404.html'), 404

# Register blueprint(s)
app.register_blueprint(tags_endpoint)
app.register_blueprint(jobs_endpoint)
app.register_blueprint(stats_endpoint)


# app.register_blueprint(authentication_endpoint)
