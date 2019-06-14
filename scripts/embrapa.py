from datetime import datetime
from osgeo import ogr
from postgis import PostgisStorager
import os
import json


def is_shapefile(f):
    return f.endswith('.shp')


class Embrapa(object):
    def __init__(self, directory):
        self._directory = directory
        self._datasets = []
        self._sample_classes = []
        self._postgis = PostgisStorager()
        self._postgis.connect()

    def get_files(self):
        files = os.listdir(self._directory)

        return [f for f in files if is_shapefile(f)]

    def _load_classes_from_db(self):
        self._sample_classes = self._postgis.execute('SELECT * FROM bdc.luc_class')
        self._samples_map_id = {}

        for sample in self._sample_classes:
            self._samples_map_id[sample["class_name"]] = sample["id"]

    def load_classes(self, ogr_file):
        """Load Samples Classes in memory
        :param ogr_file
        """
        layer_name = ogr_file.GetName()[:-4].split('/')[-1]

        self._load_classes_from_db()

        unique_classes = ogr_file.ExecuteSQL('SELECT DISTINCT CLASS_INPE FROM {}'.format(layer_name))

        samples_to_save = []

        for feature_id in range(unique_classes.GetFeatureCount()):
            feature = unique_classes.GetFeature(feature_id)
            class_name = feature.GetField(0)

            # When class already registered, skips
            if class_name in self._samples_map_id.keys():
                continue

            sample_class = {
                "class_name": class_name,
                "description": class_name,
                "luc_classification_system_id": 1  # TODO Change to dynamic value
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self._postgis.insert_many("""
                INSERT INTO bdc.luc_class ( class_name, description, luc_classification_system_id )
                     VALUES (%(class_name)s, %(description)s, %(luc_classification_system_id)s )
            """, samples_to_save)

            # TODO: Remove it and make object key id manually
            self._load_classes_from_db()

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

                dataset = {
                    "start_date": datetime.strptime(start_date, '%Y-%m-%d'),
                    "end_date": datetime.strptime(end_date, '%Y-%m-%d'),
                    "lat": properties["LAT"],
                    "long": properties["LON"],
                    "srid": int(layer.GetSpatialRef().GetAuthorityCode(None)),
                    "class_id": self._samples_map_id[properties["CLASS_INPE"]]
                }

                self._datasets.append(dataset)

    def load_datasets(self):
        files = self.get_files()

        for f in files:
            self.load(f)

        return self

    def store(self):
        self._postgis.insert_many('''
            INSERT INTO bdc.observation ( start_date, end_date, location, class_id )
                 VALUES (%(start_date)s,
                         %(end_date)s,
                         ST_Transform(
                             ST_SetSRID(
                                ST_MakePoint(%(long)s, %(lat)s),
                                 %(srid)s
                             ),
                             4326
                         ),
                         %(class_id)s )
        ''', self._datasets)


embrapa = Embrapa('/data/samples/Embrapa/Pontos_Coletados_Embrapa')

embrapa.load_datasets()
embrapa.store()