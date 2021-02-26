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
from sqlalchemy import (JSON, Column, Date, ForeignKey, Integer, String, Text,
                        select)
from sqlalchemy.sql import and_
from sqlalchemy_utils import create_view

from sample_db.models.users import Users

from ..config import Config


class CollectMethod(BaseModel):
    """Datasets Model."""

    __tablename__ = 'collect_method'
    __table_args__ = {'schema': Config.SAMPLEDB_SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)


class Datasets(BaseModel):
    """Datasets Model."""

    __tablename__ = 'datasets'
    __table_args__ = {'schema': Config.SAMPLEDB_SCHEMA}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id,
                                         ondelete='NO ACTION'), nullable=False)
    classification_system_id = Column(Integer, ForeignKey(LucClassificationSystem.id,
                                                          ondelete='NO ACTION'), nullable=False)
    collect_method_id = Column(Integer, ForeignKey(CollectMethod.id,
                                                   ondelete='NO ACTION'), nullable=True)

    name = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    observation_table_name = Column(String, nullable=False)
    midias_table_name = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    version = Column(String, nullable=True)
    description = Column(Text, nullable=True)


class DatasetView(BaseModel):
    __tablename__ = 'v_dataset'

    __table__ = create_view(
        name=__tablename__,
        selectable=select([Datasets.created_at,
                           Datasets.updated_at,
                           Datasets.id,
                           Datasets.name,
                           Datasets.start_date,
                           Datasets.end_date,
                           Datasets.observation_table_name,
                           Datasets.midias_table_name,
                           Datasets.metadata_json,
                           Datasets.version,
                           Datasets.description,
                           LucClassificationSystem.name.label('classification_system_name'),
                           Users.full_name.label('user_name'),
                           CollectMethod.name.label('collect_method')]
                          ).where(and_(Users.id == Datasets.user_id,
                                       LucClassificationSystem.id == Datasets.classification_system_id,
                                       CollectMethod.id == Datasets.collect_method_id)),
        metadata=BaseModel.metadata,
    )
    __table__.schema = Config.SAMPLEDB_SCHEMA
