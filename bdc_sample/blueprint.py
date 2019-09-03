from flask import Blueprint
from flask_restplus import Api
from bdc_sample.controller import ns as sample_ns


bp = Blueprint('sample', __name__, url_prefix='/sample')

api = Api(bp, doc=False)

api.add_namespace(sample_ns)