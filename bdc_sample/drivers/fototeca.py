from bdc_sample.core.driver import CSVDriver
import os


class Fototeca(CSVDriver):
    """
    Driver for Fototeca Sample for data loading to `sampledb`
    """
    def __init__(self, directory, storager, user, system):
        """
        Create Fototeca Samples data handlers
        :param directory: string Directory where converted files will be stored
        :param storager: PostgisAccessor
        """
        super().__init__(directory, storager, user, system)

        storager.open()

    def get_unique_classes(self, csv):
        return csv['label'].unique()

    def build_data_set(self, csv):
        csv['srid'] = 4326
        csv['class_id'] = csv['label'].apply(lambda row: self.storager.samples_map_id[row])
        csv['user_id'] = 1
        csv['lat'] = csv['latitude']
        csv['long'] = csv['longitude']
        return csv