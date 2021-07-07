#
# This file is part of Sample Database.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Sample-DB utils for accessor."""

from lccs_db.models import LucClass
from lccs_db.models import db as _db


class DBAccessor(object):
    """DBAccessor Class."""

    def __init__(self, system_id=None):
        """Init method."""
        self.sample_classes = []
        self.samples_map_id = {}
        self.classification_system_id = system_id

    def store_classes(self, classes):
        """Insert multiple sample classes on database.

        Args:
            classes (dict[]): list List of classes objects to save
        """
        _db.session.bulk_insert_mappings(LucClass, classes)
        _db.session.commit()

    def store_data(self, data_sets, dataset_table):
        """Store sample data into database.

        Args:
            data_sets (dict[]): List of data sets observation to store
            dataset_table (table): Dataset table to insert
        """
        _db.engine.execute(
            dataset_table.insert(),
            data_sets
        )
        _db.session.commit()

    def load(self):
        """Load sample classes in memory."""
        if self.classification_system_id:
            self.sample_classes = LucClass.filter(class_system_id=self.classification_system_id)
        else:
            self.sample_classes = LucClass.filter()
        self.samples_map_id = {}

        for sample in self.sample_classes:
            self.samples_map_id[sample.name.capitalize()] = sample.id