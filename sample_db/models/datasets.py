#
# This file is part of SAMPLE-DB.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""SampleDB Datasets Model."""
import json
import pkgutil
from typing import Dict, Iterable, Union

from bdc_db.sqltypes import JSONB
from jsonschema import draft7_format_checker
from lccs_db.models import LucClass, LucClassificationSystem
from lccs_db.models.base import BaseModel
from sqlalchemy import (ARRAY, JSON, Boolean, Column, Date, Enum, ForeignKey,
                        Index, Integer, String, Table, Text, UniqueConstraint,
                        select)
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.sql import and_, func
from sqlalchemy_utils import create_view
from sqlalchemy_views import CreateView

from ..config import Config
from .base import db as _db
from .dataset_table import make_dataset_table
from .users import Users

Feature = Dict[str, str]

enum_status_type = Enum('IN_PROGRESS', 'PUBLISHED', 'IN_REVISION', name='status_type')

class CollectMethod(BaseModel):
    """Collect Method Model."""

    __tablename__ = 'collect_method'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        Index(None, name),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )


class Datasets(BaseModel):
    """Datasets Model."""

    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    dataset_table_id = Column(OID, nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String, nullable=False)
    version_predecessor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    version_successor = Column(ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'))
    is_public = Column(Boolean(), nullable=False, default=False)
    users = Column(ARRAY(Integer), nullable=True)
    status = Column(enum_status_type, nullable=False)
    properties = Column(JSONB(schema='sampledb/properties.json',
                                 draft_checker=None), nullable=True)
    metadata_json = Column(JSONB(schema='sampledb/metadata.json',
                                 draft_checker=None), nullable=True)
    classification_system_id = Column(Integer,
                                      ForeignKey(LucClassificationSystem.id, ondelete='CASCADE', onupdate='CASCADE'),
                                      nullable=False)
    collect_method_id = Column(Integer, ForeignKey(CollectMethod.id, ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=True)
    user_id = Column(Integer, ForeignKey(Users.user_id, ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        Index(None, user_id),
        Index(None, classification_system_id),
        Index(None, collect_method_id),
        Index(None, name),
        UniqueConstraint('name', 'version'),
        Index('idx_datasets_start_date_end_date', start_date, end_date),
        Index(None, start_date.desc()),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )

    @classmethod
    def create_ds_table(cls, table_name: str, version: str, **kwargs) -> 'Datasets':
        """Create an sample table to store and retrieve a respective dataset instance.

        Args:
            table_name - Dataset name (Used as table_name).
            version - Dataset version.
        """
        ds = cls()
        ds.name = table_name
        ds.version = version

        ds_table_name = f'{table_name.replace("-", "_")}_{version}'

        ds_table, _ = make_dataset_table(f'{ds_table_name.lower()}', create=True)

        table_id = cls.get_table_id(ds_table_name)

        ds.dataset_table_id = table_id

        return ds

    @classmethod
    def get_table_id(cls, ds_table_name: str) -> str:
        """Retrieve a Table OID from a sample dataset name.

        Raises:
            Exception when there is no sample table for ds name.
        """
        res = _db.session.execute(
            f'SELECT \'{Config.SAMPLEDB_SCHEMA}.dataset_{ds_table_name.lower()}\'::regclass::oid AS table_id'
        ).first()

        if res.table_id is None:
            raise RuntimeError(f'Table oid is null')

        return res.table_id

    @classmethod
    def get_ds_table(cls, ds_name: str, ds_version: str) -> Union[Table, None]:
        """Retrieve the sample dataset table based in the given name and version.

        Notes:
            It does not raise error when dataset does not exist.

        Args:
            ds_name: The Dataset name
            ds_version: The Dataset version
        Returns:
            Table: A SQLAlchemy table reference to dataset geometry table.
        """
        expr = 'SELECT relname AS table_name, ' \
               'relnamespace::regnamespace::text AS schema ' \
               f'FROM {Config.SAMPLEDB_SCHEMA}.datasets as ds, pg_class ' \
               f'WHERE ds.dataset_table_id = pg_class.oid AND ' \
               f'LOWER(ds.name) = LOWER(\'{ds_name}\') AND ' \
               f'LOWER(ds.version) = LOWER(\'{ds_version}\')'

        try:
            res =  _db.session.execute(expr).fetchone()
            if res:
                return Table(res.table_name, _db.metadata, schema=Config.SAMPLEDB_SCHEMA, autoload=True,
                             autoload_with=_db.engine)

            return None
        finally:
            _db.session.close()

    @property
    def ds_table(self) -> Union[Table, None]:
        """Retrieve instance dataset table."""
        return self.get_ds_table(self.name, self.version)

    @property
    def insert_ds_table(self, features: Iterable[Feature], **kwargs) -> None:
        """Insert data into dataset table."""

        ds = self.ds_table

        _db.session.execute(ds.insert().values(features))

    @property
    def make_view_dataset_data(self) -> Table:
        """Create a view of an observation model using a table name."""

        # reflect dataset table
        dt_table = self.ds_table

        selectable = select([dt_table.c.id,
                             dt_table.c.start_date,
                             dt_table.c.end_date,
                             dt_table.c.collection_date,
                             dt_table.c.user_id.label('user_id'),
                             dt_table.c.class_id.label('class_id'),
                             LucClass.name.label('class_name'),
                             func.Geometry(dt_table.c.location).label('location'),
                             ]).where(LucClass.id == dt_table.c.class_id)

        view_table = Table(f'view_{dt_table.name}', _db.metadata, schema=Config.SAMPLEDB_SCHEMA)

        try:
            dt_view = CreateView(view_table, selectable)

            # _db.engine.execute(dt_view)
        except BaseException as err:
            _db.session.rollback()
            raise RuntimeError('Error while create the dataset view')

        return dt_view


class DatasetView(BaseModel):
    """Datasets View Model."""

    __tablename__ = 'v_datasets'

    __table__ = create_view(
        name=__tablename__,
        selectable=select([Datasets.created_at,
                           Datasets.updated_at,
                           Datasets.id,
                           Datasets.name,
                           Datasets.title,
                           Datasets.is_public,
                           Datasets.start_date,
                           Datasets.end_date,
                           Datasets.dataset_table_id,
                           Datasets.metadata_json,
                           Datasets.version,
                           Datasets.version_successor,
                           Datasets.version_predecessor,
                           Datasets.description,
                           Datasets.user_id,
                           Datasets.classification_system_id.label('classification_system_id'),
                           LucClassificationSystem.name.label('classification_system_name'),
                           LucClassificationSystem.version.label('classification_system_version'),
                           Datasets.collect_method_id.label('collect_method_id'),
                           CollectMethod.name.label('collect_method_name')]
                          ).where(and_(LucClassificationSystem.id == Datasets.classification_system_id,
                                       CollectMethod.id == Datasets.collect_method_id)),
        metadata=BaseModel.metadata,
    )
    __table__.schema = Config.SAMPLEDB_SCHEMA
