import re
from datetime import datetime
from os import path
from osgeo import ogr
from shapely.wkt import loads
from geoalchemy2 import shape
from bdc_sample.core.driver import ShapeToTableDriver


class Cerrado(ShapeToTableDriver):
    """Driver for Cerrado Sample for data loading to `sampledb`"""

    start_date = None
    end_date = None
    class_name = 'CLASSE PRI'

    def load(self, file):
        file_name = path.splitext(path.basename(file))[0]

        matched = re.search(r'.*?(\d+)$', file_name)

        if matched.group(1):
            year = int(matched.group(1))

            self.start_date = datetime(year=year, month=1, day=1)
            self.end_date = datetime(year=year, month=12, day=31)
        else:
            self.start_date = self.end_date = datetime.utcnow()

        return super(Cerrado, self).load(file)

    def get_unique_classes(self, ogr_file, layer_name):
        return ogr_file.ExecuteSQL(
            'SELECT DISTINCT "{}" FROM {}'.format(self.class_name, layer_name))

    def build_data_set(self, feature, **kwargs):
        multipoint = feature.GetGeometryRef()
        point = multipoint.GetGeometryRef(0)

        shapely_point = loads(point.ExportToWkt()).representative_point()
        ewkt = shape.from_shape(shapely_point, srid=4326)

        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": ewkt,
            "class_id": self.storager.samples_map_id[feature.GetField(self.class_name)],
            "user_id": self.user.id
        }