from bdc_sample.core.driver import CSVDriver
from geopandas import GeoDataFrame
from shapely.geometry import Point


class CSV(CSVDriver):
    def __init__(self, mappings, directory, storager, **kwargs):
        super(CSV, self).__init__(directory, storager, **kwargs)

        self.mappings = mappings

    def build_data_set(self, csv):
        geom_column = [Point(xy) for xy in zip(csv['longitude'], csv['latitude'])]
        geocsv = GeoDataFrame(csv, crs=self.mappings.get('srid', 4326), geometry=geom_column)

        geocsv['location'] = geocsv['geometry'].apply(lambda point: ';'.join(['SRID=4326', point.wkt]))
        geocsv['class_id'] = geocsv[self.mappings['class_name']].apply(lambda row: self.storager.samples_map_id[row])
        geocsv['user_id'] = self.user.id

        # Delete id column to avoid DuplicateError on database
        del geocsv['id']

        return geocsv

    def get_unique_classes(self, csv):
        """Retrieves distinct sample classes from CSV datasource"""
        return csv[self.mappings['class_name']]