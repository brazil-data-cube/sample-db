#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Midias Model."""

from typing import Callable

from sqlalchemy import Column, ForeignKey, Integer, String, Table

from lccs_db.models import db

from .base import metadata


def make_midias(table_name: str, observation: Table, create: bool = False) -> Table:
    """Create customized midia model using a table name.
    TODO: Create an example
    Args:
        table_name - Table name
        observation - SQLALchemy Table Observation
        create - Flag to create if not exists
    Returns
        Observation definition
    """

    klass = Table('{}_midias'.format(table_name), metadata,
        Column('id', Integer, primary_key=True),
        Column(
            'observation_id',
            Integer,
            ForeignKey(observation.id, ondelete='NO ACTION', onupdate='CASCADE'),
            nullable=False
        ),
        Column('url', String, nullable=False),
    )

    if create:
        if not klass.exists(bind=db.engine):
            klass.create(bind=db.engine)

    return klass