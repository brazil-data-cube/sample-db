"""
Samples Cerrado
"""

from os import path
from re import search as regex_search
from datetime import datetime
from geoalchemy2 import shape
from shapely.wkt import loads as geom_from_wkt
from bdc_sample.core.driver import Shapefile


class Cerrado(Shapefile):
    """Driver for Cerrado Sample for data loading to `sampledb`"""

    def __init__(self, entries, **kwargs):
        mappings = dict(class_name='CLASSE PRI')

        super(Cerrado, self).__init__(entries, mappings, **kwargs)

    def load(self, file):
        file_name = path.splitext(path.basename(file))[0]

        matched = regex_search(r'.*?(\d+)$', file_name)

        if matched.group(1):
            year = int(matched.group(1))

            self.mappings['start_date'].setdefault(
                'value',
                datetime(year=year, month=1, day=1))

            self.mappings['end_date'].setdefault(
                'value',
                datetime(year=year, month=12, day=31))
        else:
            now = datetime.utcnow()
            self.mappings['start_date'].setdefault('value', now)
            self.mappings['end_date'].setdefault('value', now)

        return super(Cerrado, self).load(file)

    def build_data_set(self, feature, **kwargs):
        multipoint = feature.GetGeometryRef()
        point = multipoint.GetGeometryRef(0)

        shapely_point = geom_from_wkt(
            point.ExportToWkt()).representative_point()
        ewkt = shape.from_shape(shapely_point, srid=4326)

        start_date = self.mappings['start_date'].get('value') or \
            feature.GetField(self.mappings['start_date']['key'])

        end_date = self.mappings['end_date'].get('value') or \
            feature.GetField(self.mappings['end_date']['key'])

        return {
            "start_date": start_date,
            "end_date": end_date,
            "location": ewkt,
            "class_id": self.storager.samples_map_id[feature.GetField(self.class_name)],
            "user_id": self.user.id
        }