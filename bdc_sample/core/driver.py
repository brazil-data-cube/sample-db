from abc import abstractmethod, ABCMeta
from osgeo import ogr
import os
import pandas as pd


class Driver(metaclass=ABCMeta):
    def __init__(self, storager, user=1, system=1):
        self.storager = storager
        self.user = user
        self.system = system
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
            print("{} loaded in memory".format(f))

        return self

    def store(self):
        self.storager.store_observations(self._data_sets)


class CSVDriver(Driver):
    def __init__(self, directory, storager, user, system):
        super().__init__(storager, user, system)

        self.directory = directory

    def get_files(self):
        files = os.listdir(self.directory)

        return [f for f in files if f.endswith(".csv")]

    @abstractmethod
    def build_data_set(self, csv):
        """Build data set sample observation"""

    @abstractmethod
    def get_unique_classes(self, csv):
        """Retrieves distinct sample classes from CSV datasource"""

    def load(self, file_name):
        absolute_file_path = os.path.join(self.directory, file_name)
        csv = pd.read_csv(absolute_file_path)

        self.load_classes(csv)

        res = self.build_data_set(csv)

        self._data_sets.extend(res.T.to_dict().values())

    def load_classes(self, csv):
        self.storager.load()

        unique_classes = self.get_unique_classes(csv)

        samples_to_save = []

        stored_keys = self.storager.samples_map_id.keys()

        for class_name in unique_classes:
            if class_name in stored_keys:
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

            # TODO: Remove it and make object key id manually
            self.storager.load()


class ShapeToTableDriver(Driver):
    def __init__(self, directory, storager, user, system):
        super().__init__(storager, user, system)

        self.directory = directory

    @abstractmethod
    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieves distinct sample classes from shapefile datasource"""

    def get_files(self):
        files = os.listdir(self.directory)

        return [f for f in files if f.endswith('.shp')]

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
                "luc_classification_system_id": self.system.id,
                "user_id": self.user.id
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self.storager.store_classes(samples_to_save)

            # TODO: Remove it and make object key id manually
            self.storager.load()