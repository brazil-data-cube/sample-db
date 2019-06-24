from bdc_sample.core.driver import ShapeToTableDriver
from datetime import datetime
from osgeo import ogr
import os
import json


class Embrapa(ShapeToTableDriver):
    """Driver for Embrapa Sample for data loading to `sampledb`"""
    def __init__(self, directory, storager, user, system):
        """
        Create Embrapa Samples data handlers
        :param directory: string Directory files containing Embrapa Samples
        :param storager: PostgisAccessor
        """
        super().__init__(directory, storager, user, system)
        self._directory = directory
        self.storager.open()

    def get_unique_classes(self, ogr_file, layer_name):
        return ogr_file.ExecuteSQL('SELECT DISTINCT CLASS_INPE FROM {}'.format(layer_name))

    def build_data_set(self, feature, **kwargs):
        layer = kwargs.get('layer')
        feature_as_json = json.loads(feature.ExportToJson())
        properties = feature_as_json['properties']

        period = properties['PERIODO'].split('-')
        start_date = '{}-01-01'.format(period[0])
        end_date = '{}-12-31'.format(period[1])

        return {
            "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
            "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
            "lat": properties["LAT"],
            "long": properties["LON"],
            "srid": int(layer.GetSpatialRef().GetAuthorityCode(None)),
            "class_id": self.storager.samples_map_id[properties["CLASS_INPE"]],
            "user_id": self.user  # TODO Change to dynamic value
        }