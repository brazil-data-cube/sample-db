"""
Samples Canasat
"""

from datetime import datetime
from shapely.geometry import Point
from bdc_sample.core.driver import ShapeToTableDriver
from bdc_sample.core.utils import reproject


class Canasat(ShapeToTableDriver):
    """
    Driver for data loading of Canasat to `sampledb`
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 directory,
                 storager,
                 user=None,
                 system=None,
                 class_name=None):
        """Constructor"""

        super().__init__(directory, storager, user, system)
        if class_name is None:
            class_name = [
                'Classe', 'Classes', 'SPRCLASSE', 'Class_map'
            ]
        if isinstance(class_name, str):
            class_name = [class_name]

        self.class_name = class_name
        self.srid = None
        self.target_class = None

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

        if layer.GetFeatureCount() == 0:
            return []

        if self.class_name is None:
            raise ValueError('Invalid class name for driver Canasat')

        f = layer.GetFeature(0)

        self.point = Canasat.point_wkt if f.GetGeometryRef().GetGeometryName() == 'POINT' else Canasat.get_centroid

        fields = [
            f.GetFieldDefnRef(i).GetName() for i in range(f.GetFieldCount())
        ]

        for possibly_class in self.class_name:
            if possibly_class in fields:
                self.target_class = possibly_class

                return ogr_file.ExecuteSQL(
                    'SELECT DISTINCT "{}" FROM {}'.format(
                        possibly_class, layer_name))
        return []


    def build_data_set(self, feature, **kwargs):
        start_date = '2015-10-01'
        end_date = '2016-07-31'
        geom = feature.GetGeometryRef()

        reproject(geom, self.srid, 4326)

        return {
            "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
            "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
            "location": ';'.join(
                ['SRID=4326', self.point(geom)]),
            "class_id": self.storager.samples_map_id[
                feature.GetFieldAsString(self.target_class)],
            "user_id": self.user.id
        }
