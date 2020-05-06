#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Datasets Model."""

from sqlalchemy import Column, Date, JSON, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import aliased
from sqlalchemy_utils import create_view

from lccs_db.models.base import BaseModel
from lccs_db.models.luc_classification_system import LucClassificationSystem
from lccs_db.models.luc_class import LucClass

from sample_db.models.users import Users

from ..config import Config


class CollectMethod(BaseModel):
    """Datasets Model."""

    __tablename__ = 'collect_method'
    __table_args__ = {'schema': Config.SAMPLEDB_ACTIVITIES_SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)

class Datasets(BaseModel):
    """Datasets Model."""

    __tablename__ = 'datasets'
    __table_args__ = {'schema': Config.SAMPLEDB_ACTIVITIES_SCHEMA}

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