#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Observations Model."""

from sqlalchemy import Column, Date, ForeignKey, Integer

from geoalchemy2 import Geometry

from sample_db.models.base import BaseModel

from ..config import Config

class Observation(BaseModel):
    """Observation Model."""

    __tablename__ = 'observations'
    __table_args__ = {'schema': Config.ACTIVITIES_SCHEMA}

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    collection_date = Column(Date, nullable=False)
    location = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
    class_system_id = Column(Integer, ForeignKey('lccs.classes.id',
                                                 ondelete='NO ACTION'), nullable=False)
    user_id = Column(Integer, ForeignKey('{}.users.id'.format(Config.ACTIVITIES_SCHEMA),
                                                 ondelete='NO ACTION'), nullable=False)