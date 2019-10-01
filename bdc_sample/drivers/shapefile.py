import os
import zipfile
from io import IOBase
from tempfile import TemporaryDirectory, SpooledTemporaryFile

from osgeo import ogr
from werkzeug import FileStorage
from bdc_sample.core.driver import ShapeToTableDriver


class Shapefile(ShapeToTableDriver):
    def __init__(self, mappings, directory, storager, **properties):
        # self.mappings = validate(mappings)
        self.mappings = mappings

        super(Shapefile, self).__init__(directory, storager, **properties)
        # self.entries = entries
        self._temporary_dirs = []

    @staticmethod
    def get_centroid(geom):
        return geom.Centroid().ExportToWkt()

    @staticmethod
    def point_wkt(geom):
        return Point(geom.GetX(), geom.GetY()).wkt

    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieves distinct sample classes from shapefile datasource"""
        layer = ogr_file.GetLayer(layer_name)

        code = layer.GetSpatialRef().GetAuthorityCode(None)

        self.srid = 4326
        if code is not None:
            self.srid = int(code) or self.srid

        if layer.GetFeatureCount() == 0:
            return []

        f = layer.GetFeature(0)

        self.point = Shapefile.point_wkt if f.GetGeometryRef().GetGeometryName() == 'POINT' else Shapefile.get_centroid

        fields = [
            f.GetFieldDefnRef(i).GetName() for i in range(f.GetFieldCount())
        ]

        for possibly_class in self.mappings['class_name']:
            if possibly_class in fields:
                self.target_class = possibly_class

                return ogr_file.ExecuteSQL(
                    'SELECT DISTINCT "{}" FROM {}'.format(
                        possibly_class, layer_name))
        return []

    @staticmethod
    def list_shapefiles(directory):
        files = os.listdir(directory)
        return [
            os.path.join(directory, f) for f in files if f.endswith('.shp')
        ]

    def get_files(self):
        if isinstance(self.directory, FileStorage):
            # if self.directory.endswith('zip'):

            temp_dir = TemporaryDirectory()

            shapefile_zip = zipfile.ZipFile(self.directory)

            shapefile_zip.extractall(temp_dir.name)

            self._temporary_dirs.append(temp_dir)

            return Shapefile.list_shapefiles(temp_dir.name)

        if isinstance(self.directory, IOBase) or \
           isinstance(self.directory, SpooledTemporaryFile) or \
           (os.path.isfile(self.directory) and self.directory.endswith('.shp')):
            return [self.directory]

        files = os.listdir(self.directory)

        return [
            os.path.join(self.directory, f) for f in files if f.endswith('.shp')
        ]

    def build_data_set(self, feature, **kwargs):
        """Build data set sample observation"""
        return feature

    def load(self, file):
        gdal_file = ogr.Open(file)

        self.load_classes(gdal_file)

        for layer_id in range(gdal_file.GetLayerCount()):
            layer = gdal_file.GetLayer(layer_id)

            for feature in layer:
                dataset = self.build_data_set(feature, **{"layer": layer})
                self._data_sets.append(dataset)

    def load_classes(self, file):
        # Retrieves Layer Name from Data set filename
        layer_name = os.path.basename(file.GetName()[:-4].split('/')[-1])
        # Load Storager classes in memory
        self.storager.load()

        unique_classes = self.get_unique_classes(file, layer_name)

        samples_to_save = []

        for feature_id in range(unique_classes.GetFeatureCount()):
            feature = unique_classes.GetFeature(feature_id)
            class_name = feature.GetField(0)

            # When class already registered, skips
            if class_name in self.storager.samples_map_id.keys():
                continue

            sample_class = {
                "class_name": class_name,
                "description": class_name,
                "luc_classification_system_id": self.system.id,
                "user_id": self.user.id
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self.storager.store_classes(samples_to_save)
            self.storager.load()
