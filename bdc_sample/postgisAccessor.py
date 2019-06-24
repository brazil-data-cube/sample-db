from postgis import Postgis


class PostgisAccessor(object):
    def __init__(self, host='localhost', port=5432, username='postgres', password='', database='amostras'):
        self._driver = Postgis(host, port, username, password, database)
        self._sample_classes = []
        self.samples_map_id = {}

    def __del__(self):
        self.close()

    def open(self):
        self._driver.connect()

    def close(self):
        self._driver.disconnect()

    def store_classes(self, classes):
        self._driver.insert_many("""
            INSERT INTO bdc.luc_class ( class_name, description, luc_classification_system_id, user_id )
                 VALUES (%(class_name)s, %(description)s, %(luc_classification_system_id)s, %(user_id)s )
        """, classes)

    def store_observations(self, data_sets):
        """
        Stores sample observation into database.
        **Note** that you must provide `lat/long` and `srid` attributes to build a location.

        TODO: Allow to handle both `lat/long` and `geom` field in data set
        :param data_sets: List of data sets observation to insert in database
        :return:
        """
        self._driver.insert_many('''
            INSERT INTO bdc.observation ( start_date, end_date, location, class_id, user_id )
                 VALUES (%(start_date)s,
                         %(end_date)s,
                         ST_Transform(
                             ST_SetSRID(
                                ST_MakePoint(%(long)s, %(lat)s),
                                 %(srid)s
                             ),
                             4326
                         ),
                         %(class_id)s,
                         %(user_id)s)
        ''', data_sets)

    def load(self):
        self._sample_classes = self._driver.execute('SELECT * FROM bdc.luc_class')
        self.samples_map_id = {}

        for sample in self._sample_classes:
            self.samples_map_id[sample["class_name"]] = sample["id"]