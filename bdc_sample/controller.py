# Python dependencies
from json import loads as resource_parse_json

# 3rdparty dependencies
from flask import request
from flask_restplus import Namespace
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest, NotFound

# Brazil Data Cube - Core Module
from bdc_core.utils.flask import APIResource

# Brazil Data Cube - SampleDB
from bdc_sample.core.driver import Driver
from bdc_sample.core.postgis_accessor import PostgisAccessor
from bdc_sample.drivers import factory
from bdc_sample.models import LucClassificationSystem, User


ns = Namespace('sample', description='sample')


@ns.route('/')
class SampleResource(APIResource):
    def post(self):
        """
        Handler of Sample upload

        Expects the following body information:
            - mappings: Mappings dict describing the sample keys
            - file: File Storage Uploaded
            - user: User
            - classification_system: Classification System Name
        """

        accessor = PostgisAccessor()

        # Provided Mappings to the driver
        mappings = resource_parse_json(request.form.get('mappings', ''))

        classification_system = request.form.get('classification_system')

        try:
            system = LucClassificationSystem.get(
                system_name=classification_system)
        except NoResultFound:
            raise NotFound('Classification system "{}" not found'.format(
                classification_system))

        try:
            user = User.get(email='admin@admin.com')
        except NoResultFound:
            raise NotFound('User "{}" not found'.format(
                'admin@admin.com'))

        # Retrieves file upload
        file = request.files.get('file')

        if not file:
            raise BadRequest('No file sample provided')

        # Retrieves factory driver backend
        driver_klass = factory.get(file.content_type)
        # Build datasource
        driver: Driver = driver_klass(entries=file,
                                      mappings=mappings,
                                      storager=accessor,
                                      user=user,
                                      system=system)
        # Load data set in memory
        driver.load_data_sets()
        # Store in database
        driver.store()

        affected_rows = len(driver.get_data_sets())

        return {"status": "success", "affected": affected_rows}, 201
