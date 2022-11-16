#
# This file is part of SAMPLE-DB.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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

    def load(self):
        """Load sample classes in memory."""
        if self.classification_system_id:
            self.sample_classes = LucClass.filter(class_system_id=self.classification_system_id)
        else:
            self.sample_classes = LucClass.filter()
        self.samples_map_id = {}

        for sample in self.sample_classes:
            self.samples_map_id[sample.name.capitalize()] = sample.id