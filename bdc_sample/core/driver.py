from abc import abstractmethod, ABCMeta
from osgeo import ogr
import os

class Driver(metaclass=ABCMeta):
    def __init__(self, storager):
        self.storager = storager
        self._data_sets = []

    @abstractmethod
    def load(self, file):
        """Opens the file and load data"""

    @abstractmethod
    def load_classes(self, file):
        """Load sample classes in memory"""

    @abstractmethod
    def get_files(self):
        """Retrieves list of files to load"""

    def load_data_sets(self):
        """Load data sets in memory using database format"""
        files = self.get_files()

        for f in files:
            self.load(f)

        return self

    def store(self):
        self.storager.store_observations(self._data_sets)


class ShapeToTableDriver(Driver):
    def __init__(self, directory, storager):
        super().__init__(storager)

        self.directory = directory

    @abstractmethod
    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieves distinct sample classes from shapefile datasource"""

    def get_files(self):
        files = os.listdir(self.directory)

        return [f for f in files if f.endswith('.shp')]

    # def build_data_set(lat, long, start_date, end_date, class_id, user_id=1, srid=4326):
    @abstractmethod
    def build_data_set(self, feature, **kwargs):
        """Build data set sample observation"""

    def load(self, filename):
        absolute_filename = os.path.join(self.directory, filename)
        gdal_file = ogr.Open(absolute_filename)

        self.load_classes(gdal_file)

        for layer_id in range(gdal_file.GetLayerCount()):
            layer = gdal_file.GetLayer(layer_id)

            for feature in layer:
                self._data_sets.append(self.build_data_set(feature, **{"layer": layer}))

    def load_classes(self, file):
        # Retrieves Layer Name from Data set filename
        layer_name = file.GetName()[:-4].split('/')[-1]
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
                "luc_classification_system_id": 1,  # TODO Change to dynamic value
                "user_id": 1  # TODO Change to dynamic value
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self.storager.store_classes(samples_to_save)

            # TODO: Remove it and make object key id manually
            self.storager.load()