#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Observations Model."""

from sqlalchemy import Column, Date, ForeignKey, Integer, Table

from geoalchemy2 import Geometry

from lccs_db.models import LucClass, db

from .base import metadata


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
        Column('user_id', Integer, primary_key=True),
        Column(
            'class_id',
            Integer,
            ForeignKey(LucClass.id, ondelete='NO ACTION', onupdate='CASCADE'),
            nullable=False
        ),
        Column('start_date', Date, nullable=False),
        Column('end_date', Date, nullable=False),
        Column('collection_date', Date, nullable=False),
        Column('location', Geometry(srid=4326))
    )

    if create:
        if not klass.exists(bind=db.engine):
            klass.create(bind=db.engine)

    return klass