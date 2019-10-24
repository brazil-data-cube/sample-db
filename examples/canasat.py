"""
Samples Canasat
"""

from geoalchemy2 import shape
from shapely.geometry import Point
from shapely.wkt import loads as geom_from_wkt
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
        self.class_name = None
        self.point = None
        self.handlers = {
            "POINT": Canasat.point_wkt,
            "POLYGON": Canasat.get_centroid
        }

    @staticmethod
    def get_centroid(geom):
        return geom.Centroid().ExportToWkt()

    @staticmethod
    def point_wkt(geom):
        return Point(geom.GetX(), geom.GetY()).wkt

    def build_data_set(self, feature, **kwargs):
        """Build data set sample observation"""
        geometry = feature.GetGeometryRef()

        point_maker = self.handlers[geometry.GetGeometryName()]
        ewkt = ';'.join(['SRID=4326', point_maker(geometry)])

        start_date = self.mappings['start_date'].get('value')

        end_date = self.mappings['end_date'].get('value')

        return {
            "start_date": start_date,
            "end_date": end_date,
            "location": ewkt,
            "class_id": self.storager.samples_map_id[feature.GetField(self.class_name)],
            "user_id": self.user.id
        }