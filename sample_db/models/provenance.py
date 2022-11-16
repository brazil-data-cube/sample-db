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
"""SampleDB Provenance Model."""
from lccs_db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Index, Integer, PrimaryKeyConstraint

from ..config import Config


class Provenance(BaseModel):
    """Provenance Model."""

    __tablename__ = 'provenance'

    dataset_id = Column(Integer, ForeignKey('{}.datasets.id'.format(Config.SAMPLEDB_SCHEMA), ondelete='CASCADE',
                                            onupdate='CASCADE'),
                        nullable=False,
                        primary_key=True)
    dataset_parent_id = Column(Integer,
                               ForeignKey('{}.datasets.id'.format(Config.SAMPLEDB_SCHEMA), ondelete='CASCADE',
                                          onupdate='CASCADE'),
                               nullable=False,
                               primary_key=True)

    __table_args__ = (
        Index(None, dataset_id),
        Index(None, dataset_parent_id),
        PrimaryKeyConstraint('dataset_id', 'dataset_parent_id'),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )
