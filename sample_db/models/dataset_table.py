#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Observations Model."""
from geoalchemy2 import Geometry
from lccs_db.config import Config as LCCSConfig
from lccs_db.models import LucClass, db
from sqlalchemy import (Column, Date, ForeignKey, ForeignKeyConstraint, Index,
                        Integer, PrimaryKeyConstraint, Sequence, Table, select)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import (AddConstraint, CreateIndex, CreateSequence,
                               _CreateDropBase)
from sqlalchemy.sql import and_, func
from sqlalchemy.types import UserDefinedType
from sqlalchemy_views import CreateView

from ..config import Config
from .base import metadata
from .users import Users


class DatasetType(UserDefinedType):
    """Custom type to create a dataset type."""

    def __init__(self):
        pass

    def get_col_spec(self):
        return "dataset_type"

    def create(self):
        if not db.engine.dialect.has_type(db.engine, self.get_col_spec(), schema=Config.SAMPLEDB_SCHEMA):
            db.engine.execute(CreateDatasetType(self))

    def drop(self):
        if db.engine.dialect.has_type(db.engine, self.get_col_spec(), schema=Config.SAMPLEDB_SCHEMA):
            db.engine.execute(DropDatasetType(self))


class CreateDatasetType(_CreateDropBase):
    pass


@compiles(CreateDatasetType)
def _create_composite_type(create, compiler, **kw):
    return f"CREATE TYPE dataset_type AS \
               ( id INTEGER, user_id INTEGER, class_id INTEGER, start_date DATE, end_date DATE, collection_date DATE, \
               location geometry(Geometry,4326))"


class DropDatasetType(_CreateDropBase):
    pass


@compiles(DropDatasetType)
def _drop_composite_type(drop, compiler, **kw):
    return 'DROP TYPE dataset_type'


def make_dataset_table(table_name: str, create: bool = False) -> Table:
    """Create customized dataset table using a table name.
    TODO: Create an example
    Args:
        table_name - Table name
        create - Flag to create if not exists
    Returns
        dataset_table definition
    """
    s_name = f"{Config.SAMPLEDB_SCHEMA}.dataset_{table_name}_id_seq"

    if create:
        if not db.engine.dialect.has_table(connection=db.engine, table_name=table_name, schema=Config.SAMPLEDB_SCHEMA):
            with db.session.begin_nested():
                db.engine.execute(f"CREATE TABLE {Config.SAMPLEDB_SCHEMA}.dataset_{table_name} OF dataset_type")
                db.engine.execute(f"CREATE SEQUENCE {s_name}")

                klass = Table(f'dataset_{table_name}', metadata, autoload=True, autoload_with=db.engine, extend_existing=True)

                # Add index, primary key and foreign key
                db.engine.execute(
                    f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER COLUMN {klass.c.class_id.name} SET NOT NULL")
                db.engine.execute(
                    f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER COLUMN {klass.c.start_date.name} SET NOT NULL")
                db.engine.execute(
                    f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER COLUMN {klass.c.end_date.name} SET NOT NULL")

                db.engine.execute(
                    f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER {klass.c.id.name} SET DEFAULT NEXTVAL('{s_name}');")

                db.engine.execute(AddConstraint(PrimaryKeyConstraint(klass.c.id)))
                db.engine.execute(CreateIndex(Index(None, klass.c.user_id)))
                db.engine.execute(CreateIndex(Index(None, klass.c.class_id)))
                db.engine.execute(CreateIndex(Index(None, klass.c.location, postgresql_using='gist')))
                db.engine.execute(CreateIndex(Index(None, klass.c.start_date)))
                db.engine.execute(CreateIndex(Index(None, klass.c.end_date)))
                db.engine.execute(CreateIndex(Index(None, klass.c.collection_date)))
                Index(f'idx_{klass.name}_start_end_date', klass.c.start_date, klass.c.end_date)
                db.engine.execute(AddConstraint(
                    ForeignKeyConstraint(name=f"dataset_{table_name}_{klass.c.user_id.name}_fkey", columns=[klass.c.user_id], refcolumns=[Users.id], onupdate="CASCADE",
                                         ondelete="CASCADE")))
                db.engine.execute(AddConstraint(
                    ForeignKeyConstraint(name=f"dataset_{table_name}_{klass.c.class_id.name}_fkey",
                                         columns=[klass.c.class_id], refcolumns=[LucClass.id], onupdate="CASCADE",
                                         ondelete="CASCADE")))

            db.session.commit()
    else:
        klass = Table(f'dataset_{table_name}', metadata, autoload=True, autoload_with=db.engine)

    return klass, s_name


def make_view_dataset_table(table_name: str, obs_table_name: str) -> bool:
    """Create a view of an observation model using a table name."""

    # reflect dataset table
    dt_table = Table(table_name, metadata, autoload=True, autoload_with=db.engine, schema=Config.SAMPLEDB_SCHEMA)

    selectable = select([dt_table.c.id,
                         dt_table.c.start_date,
                         dt_table.c.end_date,
                         dt_table.c.collection_date,
                         dt_table.c.user_id.label('user_id'),
                         Users.full_name.label('user_name'),
                         dt_table.c.class_id.label('class_id'),
                         LucClass.name.label('class_name'),
                         func.Geometry(dt_table.c.location).label('location'),
                         ]).where(and_(Users.id == dt_table.c.user_id,
                                       LucClass.id == dt_table.c.class_id))

    view_table = Table(obs_table_name, metadata, schema=Config.SAMPLEDB_SCHEMA)

    try:
        dt_view = CreateView(view_table, selectable)

        db.engine.execute(dt_view)
        return True
    except BaseException as err:
        print(err)
        raise RuntimeError('Error while create the dataset table data')
