from bdc_sample.models import db, LucClass, Observation

class PostgisAccessor(object):
    def __init__(self):
        self.sample_classes = []
        self.samples_map_id = {}

    def store_classes(self, classes):
        """
        Utility method to insert multiple sample classes on database

        Args:
            classes (dict[]): list List of classes objects to save
        """
        db.session.bulk_insert_mappings(LucClass, classes)
        db.session.commit()

    def store_observations(self, data_sets):
        """
        Stores sample observation into database.

        Args:
            data_sets (dict[]): List of data sets observation to store
        """
        db.engine.execute(
            Observation.__table__.insert(),
            data_sets
        )
        db.session.commit()

    def load(self):
        """Load sample classes in memory"""
        self.sample_classes = LucClass.filter()
        self.samples_map_id = {}

        for sample in self.sample_classes:
            self.samples_map_id[sample.class_name] = sample.id
