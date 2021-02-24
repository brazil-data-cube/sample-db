#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Observations Model."""

from geoalchemy2 import Geometry
from lccs_db.models import LucClass, db
from sqlalchemy import (Column, Date, ForeignKey, Integer, Table, and_, cast,
                        select)
from sqlalchemy.sql import and_, func
from sqlalchemy_views import CreateView, DropView

from sample_db.models.users import Users


from ..config import Config
from .base import metadata
from ..config import Config


def make_observation(table_name: str, create: bool = False) -> Table:
    """Create customized observation model using a table name.
    TODO: Create an example
    Args:
        table_name - Table name
        create - Flag to create if not exists
    Returns
        Observation definition
    """

    klass = Table('{}_observations'.format(table_name), metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('user_id', Integer, ForeignKey(Users.id, ondelete='NO ACTION', onupdate='CASCADE')),
        Column(
            'class_id',
            Integer,
            ForeignKey(LucClass.id, ondelete='NO ACTION', onupdate='CASCADE'),
            nullable=False
        ),
        Column('start_date', Date, nullable=False),
        Column('end_date', Date, nullable=False),
        Column('collection_date', Date, nullable=True),
        Column('location', Geometry(srid=4326))
    )

    if create:
        if not klass.exists(bind=db.engine):
            klass.create(bind=db.engine)

    return klass


def make_view_observation(table_name: str, obs_table_name: str) -> bool:
    """Create a view of an observation model using a table name."""

    # reflect observation table
    obs_table = Table(table_name, metadata, autoload=True, autoload_with=db.engine)

    selectable = select([obs_table.c.id,
                         obs_table.c.start_date,
                         obs_table.c.end_date,
                         obs_table.c.collection_date,
                         Users.full_name.label('user_name'),
                         LucClass.name.label('class_name'),
                         func.Geometry(obs_table.c.location).label('location'),
                         ]).where(and_(Users.id == obs_table.c.user_id,
                                       LucClass.id == obs_table.c.class_id))

    view_table = Table(obs_table_name, metadata, schema=Config.SAMPLEDB_ACTIVITIES_SCHEMA)

    try:
        obs_view = CreateView(view_table, selectable)

        db.engine.execute(obs_view)

        return True
    except:
        return False
