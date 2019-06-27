from bdc_sample.core.driver import ShapeToTableDriver
from bdc_sample.core.utils import reproject
from datetime import datetime
from osgeo import ogr
from shapely.geometry import Point
import json
import os


class Dpi(ShapeToTableDriver):
    """Driver for data loading to `sampledb`"""

    def get_unique_classes(self, ogr_file, layer_name):
        return ogr_file.ExecuteSQL('SELECT DISTINCT ext_na FROM {}'.format(layer_name))

    def build_data_set(self, feature, **kwargs):
        layer = kwargs.get('layer')

        start_date = '2015-10-01'
        end_date = '2016-07-31'
        geom = feature.GetGeometryRef()

        reproject(geom, int(layer.GetSpatialRef().GetAuthorityCode(None)) or 4326, 4326)

        return {
            "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
            "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
            # TODO: Reproject
            "location": ';'.join(['SRID=4326', Point(geom.GetX(), geom.GetY()).wkt]),
            "class_id": self.storager.samples_map_id[feature.GetFieldAsString("ext_na")],
            "user_id": self.user.id
        }