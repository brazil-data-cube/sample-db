#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Datasets Model."""

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text

from lccs_db.models.base import BaseModel
from lccs_db.models.luc_classification_system import LucClassificationSystem

from sample_db.models.users import Users

from ..config import Config

import enum

class CollectMethodEnum(enum.Enum):
    """Python Enum Class for Collect Method"""
    VISUAL = "Visual"
    IN_LOCO = "In Loco"


class Datasets(BaseModel):
    """Datasets Model."""

    __tablename__ = 'datasets'
    __table_args__ = {'schema': Config.ACTIVITIES_SCHEMA}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.id,
                                         ondelete='NO ACTION'), nullable=False)
    classification_system_id = Column(Integer, ForeignKey(LucClassificationSystem.id,
                                         ondelete='NO ACTION'), nullable=False)
    collect_method = Column(Enum(CollectMethodEnum), nullable=False)
    name = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    observation_table_name = Column(String, nullable=False)
    midias_table_name = Column(String, nullable=True)
    metadata_json = Column(String, nullable=True)
    version = Column(String, nullable=True)
    description = Column(Text, nullable=True)
