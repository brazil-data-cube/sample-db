from bdc_sample.core.driver import ShapeToTableDriver
from datetime import datetime
from osgeo import ogr
import json
import os


class Dpi(ShapeToTableDriver):
    """Driver for data loading to `sampledb`"""
    def __init__(self, directory, storager):
        """
        Create InSitu Samples data handlers
        :param directory: string Directory where converted files will be stored
        :param storager: PostgisAccessor
        """
        super().__init__(directory, storager)
        self._directory = directory
        self.storager.open()

    def get_unique_classes(self, ogr_file, layer_name):
        return ogr_file.ExecuteSQL('SELECT DISTINCT ext_na FROM {}'.format(layer_name))

    def load(self, filename):
        absolute_filename = os.path.join(self._directory, filename)
        gdal_file = ogr.Open(absolute_filename)

        # self.load_classes(gdal_file)

        for layer_id in range(gdal_file.GetLayerCount()):
            layer = gdal_file.GetLayer(layer_id)

            srid = int(layer.GetSpatialRef().GetAuthorityCode(None))

            for feature in layer:
                geom = feature.GetGeometryRef()

                start_date = '2015-10-01'
                end_date = '2016-07-31'

                data_set = {
                    "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
                    "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
                    "lat": geom.GetY(),
                    "long": geom.GetX(),
                    "srid": srid,
                    "class_id": self.storager.samples_map_id[feature.GetFieldAsString["ext_na"]],
                    "user_id": 1  # TODO Change to dynamic value
                }

                self._data_sets.append(data_set)