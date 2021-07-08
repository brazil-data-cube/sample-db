#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Datasets Model."""
from lccs_db.models.base import BaseModel
from lccs_db.models.luc_classification_system import LucClassificationSystem
from sqlalchemy import (JSON, Boolean, Column, Date, ForeignKey, Index,
                        Integer, String, Text, UniqueConstraint, select)
from sqlalchemy.sql import and_
from sqlalchemy_utils import create_view

from ..config import Config


class CollectMethod(BaseModel):
    """Collect Method Model."""

    __tablename__ = 'collect_method'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        Index(None, name),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )


class Datasets(BaseModel):
    """Datasets Model."""

    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    dataset_table_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String, nullable=False)
    version_predecessor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    version_successor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    is_public = Column(Boolean(), nullable=False, default=True)
    metadata_json = Column(JSON, nullable=True)
    classification_system_id = Column(Integer,
                                      ForeignKey(LucClassificationSystem.id, ondelete='CASCADE', onupdate='CASCADE'),
                                      nullable=False)
    collect_method_id = Column(Integer, ForeignKey(CollectMethod.id, ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        Index(None, user_id),
        Index(None, classification_system_id),
        Index(None, collect_method_id),
        Index(None, name),
        UniqueConstraint('name', 'version'),
        Index('idx_datasets_start_date_end_date', start_date, end_date),
        Index(None, start_date.desc()),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )


class DatasetView(BaseModel):
    """Datasets View Model."""

    __tablename__ = 'v_datasets'

    __table__ = create_view(
        name=__tablename__,
        selectable=select([Datasets.created_at,
                           Datasets.updated_at,
                           Datasets.id,
                           Datasets.name,
                           Datasets.title,
                           Datasets.is_public,
                           Datasets.start_date,
                           Datasets.end_date,
                           Datasets.dataset_table_name,
                           Datasets.metadata_json,
                           Datasets.version,
                           Datasets.version_successor,
                           Datasets.version_predecessor,
                           Datasets.description,
                           Datasets.user_id,
                           Datasets.classification_system_id.label('classification_system_id'),
                           LucClassificationSystem.name.label('classification_system_name'),
                           LucClassificationSystem.version.label('classification_system_version'),
                           Datasets.collect_method_id.label('collect_method_id'),
                           CollectMethod.name.label('collect_method_name')]
                          ).where(and_(LucClassificationSystem.id == Datasets.classification_system_id,
                                       CollectMethod.id == Datasets.collect_method_id)),
        metadata=BaseModel.metadata,
    )
    __table__.schema = Config.SAMPLEDB_SCHEMA
