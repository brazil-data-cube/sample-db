from datetime import datetime
from osgeo import ogr
import os
import json


def is_shapefile(f):
    return f.endswith('.shp')


class Embrapa(object):
    """

    """
    def __init__(self, directory, storager):
        """
        Create Embrapa Samples data handlers
        :param directory: string Directory files containing Embrapa Samples
        :param storager: PostgisAccessor
        """
        self._directory = directory
        self._data_sets = []
        self._sample_classes = []
        self._storager = storager
        self._storager.open()

    def get_files(self):
        files = os.listdir(self._directory)

        return [f for f in files if is_shapefile(f)]

    def load_classes(self, ogr_file):
        """Load Samples Classes in memory
        :param ogr_file
        """

        # Retrieves Layer Name from Data set filename
        layer_name = ogr_file.GetName()[:-4].split('/')[-1]
        # Load Storager classes in memory
        self._storager.load()

        unique_classes = ogr_file.ExecuteSQL('SELECT DISTINCT CLASS_INPE FROM {}'.format(layer_name))

        samples_to_save = []

        for feature_id in range(unique_classes.GetFeatureCount()):
            feature = unique_classes.GetFeature(feature_id)
            class_name = feature.GetField(0)

            # When class already registered, skips
            if class_name in self._storager.samples_map_id.keys():
                continue

            sample_class = {
                "class_name": class_name,
                "description": class_name,
                "luc_classification_system_id": 1  # TODO Change to dynamic value
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self._storager.store_classes(samples_to_save)

            # TODO: Remove it and make object key id manually
            self._storager.load()

    def load(self, filename):
        absolute_filename = os.path.join(self._directory, filename)
        gdal_file = ogr.Open(absolute_filename)

        self.load_classes(gdal_file)

        for layer_id in range(gdal_file.GetLayerCount()):
            layer = gdal_file.GetLayer(layer_id)

            for feature_id in range(layer.GetFeatureCount()):
                feature = layer.GetFeature(feature_id)

                feature_as_json = json.loads(feature.ExportToJson())
                properties = feature_as_json['properties']

                period = properties['PERIODO'].split('-')
                start_date = '{}-01-01'.format(period[0])
                end_date = '{}-12-31'.format(period[1])

                data_set = {
                    "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
                    "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
                    "lat": properties["LAT"],
                    "long": properties["LON"],
                    "srid": int(layer.GetSpatialRef().GetAuthorityCode(None)),
                    "class_id": self._storager.samples_map_id[properties["CLASS_INPE"]]
                }

                self._data_sets.append(data_set)

    def load_data_sets(self):
        files = self.get_files()

        for f in files:
            self.load(f)

        return self

    def store(self):
        self._storager.store_observations(self._data_sets)