from bdc_sample.core.driver import CSVDriver
from geopandas import GeoDataFrame
from shapely.geometry import Point
import os


class Fototeca(CSVDriver):
    """
    Driver for Fototeca Sample for data loading to `sampledb`
    """
    def get_unique_classes(self, csv):
        """Retrieve unique classes from Fototeca sample driver. By default: `label`"""
        return csv['label'].unique()

    def build_data_set(self, csv):
        geom_column = [Point(xy) for xy in zip(csv['longitude'], csv['latitude'])]
        geocsv = GeoDataFrame(csv, crs=4326, geometry=geom_column)

        geocsv['location'] = geocsv['geometry'].apply(lambda point: ';'.join(['SRID=4326', point.wkt]))

        geocsv['class_id'] = geocsv['label'].apply(lambda row: self.storager.samples_map_id[row])
        geocsv['user_id'] = self.user.id
        return geocsv
