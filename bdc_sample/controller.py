from json import loads as resource_parse_json
from bdc_core.utils.flask import APIResource
from bdc_sample.core.driver import Driver
from bdc_sample.core.postgis_accessor import PostgisAccessor
from bdc_sample.drivers import factory
from bdc_sample.models import LucClassificationSystem, User, db
from flask import request
from flask_restplus import Namespace


ns = Namespace('', description='sample')


@ns.route('/')
class SampleResource(APIResource):
    def post(self):
        accessor = PostgisAccessor()

        mappings = resource_parse_json(request.form.get('mappings', ''))

        system = db.session.query(LucClassificationSystem).filter(LucClassificationSystem.system_name == 'vmaus').first()
        user = db.session.query(User).filter(User.email == 'admin@admin.com').first()

        files_key = next(request.files.keys())

        for file_storage in request.files.getlist(files_key):
            driver: Driver = factory.get(file_storage.content_type)(directory=file_storage, mappings=mappings, storager=accessor, user=user, system=system)

            driver.load_data_sets()

            driver.store()

        return {"status": "success"}, 201