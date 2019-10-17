"""
Samples Canasat
"""

from datetime import datetime
from shapely.geometry import Point
from bdc_sample.core.driver import Shapefile
from bdc_sample.core.utils import reproject


class Canasat(Shapefile):
    """
    Driver for data loading of Canasat to `sampledb`
    """

    def __init__(self, entries, **kwargs):
        mappings = dict(
            class_name=[
                'Classe', 'Classes', 'SPRCLASSE', 'Class_map'
            ],
            start_date=dict(value='2015-10-01'),
            end_date=dict(value='2016-07-31')
        )

        super(Canasat, self).__init__(entries, mappings, **kwargs)

        self.srid = None
        self.target_class = None
        self.point = None


    @staticmethod
    def get_centroid(geom):
        return geom.Centroid().ExportToWkt()

    @staticmethod
    def point_wkt(geom):
        return Point(geom.GetX(), geom.GetY()).wkt

    def get_unique_classes(self, ogr_file, layer_name):
        layer = ogr_file.GetLayer(layer_name)

        code = layer.GetSpatialRef().GetAuthorityCode(None)

        self.srid = 4326
        if code is not None:
            self.srid = int(code) or self.srid

        feature = layer.GetFeature(0)

        self.point = Canasat.point_wkt \
            if feature.GetGeometryRef().GetGeometryName() == 'POINT' \
            else Canasat.get_centroid

        return super(Canasat, self).get_unique_classes(ogr_file, layer_name)
