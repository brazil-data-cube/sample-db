from bdc_sample.models import db, LucClass, Observation

class PostgisAccessor(object):
    def __init__(self):
        self.sample_classes = []
        self.samples_map_id = {}

    def store_classes(self, classes):
        """
        Utility method to insert multiple sample classes on database
        :param classes: list List of classes objects to save
        """
        # for sample_class in classes:
        #     klass = LucClass(**sample_class)
        #     klass.save(commit=False)
        db.session.bulk_insert_mappings(LucClass, classes)
        # Commit transaction once
        db.session.commit()

    def store_observations(self, data_sets):
        """
        Stores sample observation into database.

        :param data_sets: List of data sets observation to insert in database
        :return:
        """
        db.session.bulk_insert_mappings(Observation, data_sets, True)
        # Commit transaction once
        db.session.commit()

    def load(self):
        """Load sample classes in memory"""
        self.sample_classes = db.session.query(LucClass).all()
        self.samples_map_id = {}

        for sample in self.sample_classes:
            self.samples_map_id[sample.class_name] = sample.id
