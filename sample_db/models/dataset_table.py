#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Observations Model."""
from geoalchemy2 import Geometry
from lccs_db.models import LucClass
from sqlalchemy import (Column, Date, ForeignKey, ForeignKeyConstraint, Index,
                        Integer, PrimaryKeyConstraint, Sequence, Table, select)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import AddConstraint, CreateIndex, _CreateDropBase
from sqlalchemy.sql import func
from sqlalchemy.types import UserDefinedType
from sqlalchemy_views import CreateView

from ..config import Config
from .base import db, metadata


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
               (created_at TIMESTAMP, updated_at TIMESTAMP, id INTEGER, user_id INTEGER, class_id INTEGER, start_date DATE, end_date DATE, collection_date DATE, \
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
        if not db.engine.dialect.has_table(connection=db.engine, table_name=f'dataset_{table_name}', schema=Config.SAMPLEDB_SCHEMA):
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
                f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER COLUMN {klass.c.created_at.name} SET DEFAULT now()")
            db.engine.execute(
                f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER COLUMN {klass.c.updated_at.name} SET DEFAULT now()")

            db.engine.execute(
                f"ALTER TABLE {Config.SAMPLEDB_SCHEMA}.{klass.name} ALTER {klass.c.id.name} SET DEFAULT NEXTVAL('{s_name}');")

            db.engine.execute(f"ALTER SEQUENCE {s_name} owned by {Config.SAMPLEDB_SCHEMA}.{klass.c.id};")

            db.engine.execute(AddConstraint(PrimaryKeyConstraint(klass.c.id)))
            db.engine.execute(CreateIndex(Index(None, klass.c.user_id)))
            db.engine.execute(CreateIndex(Index(None, klass.c.class_id)))
            db.engine.execute(CreateIndex(Index(None, klass.c.location, postgresql_using='gist')))
            db.engine.execute(CreateIndex(Index(None, klass.c.start_date)))
            db.engine.execute(CreateIndex(Index(None, klass.c.end_date)))
            db.engine.execute(CreateIndex(Index(None, klass.c.collection_date)))
            db.engine.execute(CreateIndex(Index(None, klass.c.created_at)))
            db.engine.execute(CreateIndex(Index(None, klass.c.updated_at)))
            Index(f'idx_{klass.name}_start_end_date', klass.c.start_date, klass.c.end_date)

            db.engine.execute(AddConstraint(
                ForeignKeyConstraint(name=f"dataset_{table_name}_{klass.c.class_id.name}_fkey",
                                     columns=[klass.c.class_id], refcolumns=[LucClass.id], onupdate="CASCADE",
                                     ondelete="CASCADE")))
        else:
            raise RuntimeError(f'Table {table_name} already exists')
    else:
        klass = Table(f'dataset_{table_name}', metadata, autoload=True, autoload_with=db.engine)

    return klass, s_name
