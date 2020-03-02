#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Midias Model."""

from sqlalchemy import Column, ForeignKey, Integer, String

from sample_db.models.base import BaseModel

from ..config import Config

class Midias(BaseModel):
    """Midias Model."""

    __tablename__ = 'midias'
    __table_args__ = {'schema': Config.ACTIVITIES_SCHEMA}

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    observation_id = Column(Integer, ForeignKey('{}.observations.id'.format(Config.ACTIVITIES_SCHEMA),
                                         ondelete='NO ACTION'), nullable=False)