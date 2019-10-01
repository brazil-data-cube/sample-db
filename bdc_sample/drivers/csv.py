from copy import deepcopy
from bdc_sample.core.driver import CSVDriver
from geopandas import GeoDataFrame
from shapely.geometry import Point


def validate_mappings(mappings):
    if not mappings:
        raise TypeError('Invalid mappings')

    if not mappings.get('class_name'):
        raise KeyError('Invalid mappings: Key "class_name" is required.')

    if not mappings.get('geom'):
        if not mappings.get('latitude') and not mappings.get('longitude'):
            mappings['latitude'] = 'latitude'
            mappings['longitude'] = 'longitude'

    if not mappings.get('start_date'):
        mappings['start_date'] = 'start_date'
    if not mappings.get('end_date'):
        mappings['end_date'] = 'end_date'


class CSV(CSVDriver):
    def __init__(self, mappings, directory, storager, **kwargs):
        copy_mappings = deepcopy(mappings)

        validate_mappings(mappings)

        super(CSV, self).__init__(directory, storager, **kwargs)

        self.mappings = copy_mappings

    def build_data_set(self, csv):
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