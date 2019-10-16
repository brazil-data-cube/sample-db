from datetime import datetime
from shapely import geometry
from geoalchemy2 import shape
from bdc_sample.core.driver import Shapefile


class Embrapa(Shapefile):
    """Driver for Embrapa Sample for data loading to `sampledb`"""

    def __init__(self, entries, **kwargs):
        mappings = dict(class_name="CLASS_INPE")

        super(Embrapa, self).__init__(entries, mappings, **kwargs)

    def build_data_set(self, feature, **kwargs):
        period = feature.GetField('PERIODO').split('-')
        start_date = '{}-01-01'.format(period[0])
        end_date = '{}-12-31'.format(period[1])

        point = geometry.Point(feature.GetField('LON'), feature.GetField('LAT'))
        ewkt = shape.from_shape(point, srid=4326)

        return {
            "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
            "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
            "location": ewkt,
            "class_id": self.storager.samples_map_id[feature.GetField('CLASS_INPE')],
            "user_id": self.user.id
        }
