from bdc_sample.core.driver import ShapeToTableDriver
from datetime import datetime
from osgeo import ogr
import json
import os


class Dpi(ShapeToTableDriver):
    """Driver for data loading to `sampledb`"""
    def __init__(self, directory, storager, user, system):
        """
        Create Dpi Samples data handlers
        :param directory: string Directory where converted files will be stored
        :param storager: PostgisAccessor
        """
        super().__init__(directory, storager, user, system)
        self._directory = directory
        self.storager.open()

    def get_unique_classes(self, ogr_file, layer_name):
        return ogr_file.ExecuteSQL('SELECT DISTINCT ext_na FROM {}'.format(layer_name))

    def build_data_set(self, feature, **kwargs):
        layer = kwargs.get('layer')
        srid = int(layer.GetSpatialRef().GetAuthorityCode(None)) or 4326

        start_date = '2015-10-01'
        end_date = '2016-07-31'
        geom = feature.GetGeometryRef()

        return {
            "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
            "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
            "lat": geom.GetY(),
            "long": geom.GetX(),
            "srid": srid,
            "class_id": self.storager.samples_map_id[feature.GetFieldAsString("ext_na")],
            "user_id": 1  # TODO Change to dynamic value
        }