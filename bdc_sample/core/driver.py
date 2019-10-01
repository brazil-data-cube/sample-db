"""
This file contains Brazil Data Cube drivers
to list the sample and store in database
"""

import io
import os
from abc import abstractmethod, ABCMeta
from copy import deepcopy
from osgeo import ogr
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point


class Driver(metaclass=ABCMeta):
    """Generic interface for data reader"""
    def __init__(self, storager, user=None, system=None):
        """
        Args:
            storager (Storager) - Storager Strategy. See @postgis_acessor
            user (bdc_sample.models.User) - The user instance sample owner
            system (bdc_sample.models.LucClassificationSystem)
                The land use coverage classification system
        """
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
        """
        Store the observations into database using
        Storager strategy
        """
        self.storager.store_observations(self._data_sets)


class CSV(Driver):
    """Base class for handling CSV files"""
    def __init__(self, mappings, directory, storager, user=None, system=None, **kwargs):
        copy_mappings = deepcopy(mappings)

        CSV._validate_mappings(mappings)

        super(CSV, self).__init__(storager, user, **kwargs)

        self.mappings = copy_mappings
        self.directory = directory

    @staticmethod
    def _validate_mappings(mappings):
        assert mappings
        assert 'class_name' in mappings

        if not mappings.get('geom'):
            if not mappings.get('latitude') and not mappings.get('longitude'):
                mappings['latitude'] = 'latitude'
                mappings['longitude'] = 'longitude'

        if not mappings.get('start_date'):
            mappings['start_date'] = 'start_date'
        if not mappings.get('end_date'):
            mappings['end_date'] = 'end_date'

    def get_files(self):
        import tempfile
        if isinstance(self.directory, io.IOBase) or \
           isinstance(self.directory, tempfile.SpooledTemporaryFile) or \
           os.path.isfile(self.directory):
            return [self.directory]

        files = os.listdir(self.directory)

        return [os.path.join(self.directory, f) for f in files if f.endswith(".csv")]

    def build_data_set(self, csv):
        """Build data set sample observation

        Args:
            csv(pd.DataFrame) - Open CSV file

        Returns:
            GeoDataFrame CSV with geospatial location
        """

        geom_column = [Point(xy) for xy in zip(csv['longitude'], csv['latitude'])]
        geocsv = GeoDataFrame(csv, crs=self.mappings.get('srid', 4326), geometry=geom_column)

        geocsv['location'] = geocsv['geometry'].apply(lambda point: ';'.join(['SRID=4326', point.wkt]))
        geocsv['class_id'] = geocsv[self.mappings['class_name']].apply(lambda row: self.storager.samples_map_id[row])
        geocsv['user_id'] = self.user.id
        geocsv['start_date'] = geocsv[self.mappings['start_date']]
        geocsv['end_date'] = geocsv[self.mappings['end_date']]

        del geocsv['geometry']
        del geocsv['latitude']
        del geocsv['longitude']

        # Delete id column to avoid DuplicateError on database
        if 'id' in geocsv.columns:
            del geocsv['id']

        return geocsv

    def get_unique_classes(self, csv):
        """Retrieves distinct sample classes from CSV datasource"""
        return csv[self.mappings['class_name']]

    def load(self, file):
        csv = pd.read_csv(file)

        self.load_classes(csv)

        res = self.build_data_set(csv)

        self._data_sets.extend(res.T.to_dict().values())

    def load_classes(self, file):
        self.storager.load()

        unique_classes = self.get_unique_classes(file)

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
            self.storager.load()


class ShapeToTableDriver(Driver):
    """Base class for Shapefiles Reader"""
    def __init__(self, directory, storager, user=None, system=None):
        super().__init__(storager, user, system)

        self.directory = directory

    @abstractmethod
    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieves distinct sample classes from shapefile datasource"""

    def get_files(self):
        if os.path.isfile(self.directory) and self.directory.endswith('.shp'):
            return [self.directory]

        files = os.listdir(self.directory)

        return [
            os.path.join(self.directory, f) for f in files if f.endswith('.shp')
        ]

    @abstractmethod
    def build_data_set(self, feature, **kwargs):
        """Build data set sample observation"""

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
            self.storager.load()
