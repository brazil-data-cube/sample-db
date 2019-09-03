from geopandas import GeoDataFrame
from shapely.geometry import Point
from bdc_sample.core.driver import CSVDriver


class Lapig(CSVDriver):
    """
    Driver for Lapig Sample for data loading to `sampledb`
    """
    def get_unique_classes(self, csv):
        """
        Retrieve unique classes from Lapig sample driver.

        Args:
            csv(GeoDataFrame): CSV Panda Data Frames
        Returns:
            GeoDataFrame formatted with location point
        """
        return csv['label'].unique()

    def build_data_set(self, csv):
        geom_column = [Point(xy) for xy in zip(csv['longitude'], csv['latitude'])]
        geocsv = GeoDataFrame(csv, crs=4326, geometry=geom_column)

        geocsv['location'] = geocsv['geometry'].apply(lambda point: ';'.join(['SRID=4326', point.wkt]))
        geocsv['class_id'] = geocsv['label'].apply(lambda row: self.storager.samples_map_id[row])
        geocsv['user_id'] = self.user.id

        del geocsv['id']

        return geocsv