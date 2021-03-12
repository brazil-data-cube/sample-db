#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Provenance Model."""
from lccs_db.models.base import BaseModel
from sqlalchemy import Column, ForeignKey, Index, Integer, PrimaryKeyConstraint

from ..config import Config


class Provenance(BaseModel):
    """Provenance Model."""

    __tablename__ = 'provenance'

    dataset_id = Column(Integer, ForeignKey('{}.datasets.id'.format(Config.SAMPLEDB_SCHEMA), ondelete='NO ACTION'),
                        nullable=False,
                        primary_key=True)
    dataset_parent_id = Column(Integer,
                               ForeignKey('{}.datasets.id'.format(Config.SAMPLEDB_SCHEMA), ondelete='NO ACTION'),
                               nullable=False,
                               primary_key=True)

    __table_args__ = (
        Index(None, dataset_id),
        Index(None, dataset_parent_id),
        PrimaryKeyConstraint('dataset_id', 'dataset_parent_id'),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )
