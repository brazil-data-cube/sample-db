#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils Interface for the Sample Database Model ."""
import logging

from bdc_db.db import db as _db
from lccs_db.models import LucClassificationSystem
from sqlalchemy import Table
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import DropSequence
from sqlalchemy.sql import and_

from .config import Config
from .db_util import DBAccessor
from .models import CollectMethod, Datasets, Users, make_dataset_table
from .models.base import metadata


def drop_dataset_table(dataset_data_table, sequence):
    """Drop dataset_<name>."""
    try:
        _db.session.execute(dataset_data_table.delete())
        _db.session.execute(DropSequence(sequence))
        _db.session.session.commit()
    except BaseException as err:
        logging.warning('Error while delete dataset table data')


def get_user(user_full_name):
    """Return the user object."""
    try:
        user = _db.session.query(Users) \
            .filter_by(full_name=user_full_name) \
            .one()
    except NoResultFound:
        raise RuntimeError(f'User {user_full_name} not found!')

    return user


def get_classification_system(classification_system_name, classification_system_version):
    """Return the classification system."""
    try:
        class_system = _db.session.query(LucClassificationSystem)\
            .filter_by(name=classification_system_name, version=classification_system_version)\
            .one()
    except NoResultFound:
        raise RuntimeError(f'Classification System {classification_system_name} not found!')

    return class_system


def get_collect_method(collect_method_name):
    """Return the collect method."""
    try:
        collect_method = CollectMethod.get(name=collect_method_name)
    except ValueError:
        raise RuntimeError(f'Collect Method {collect_method_name} not found!')
    return collect_method


def create_dataset_table(user_full_name, dataset_table_name, classification_system_name,
                         classification_system_version, mimetype, dataset_file, **extra_fields):
    """Insert dataset data into database."""
    from sample_db_utils.core.driver import Driver
    from sample_db_utils.factory import factory

    extra_fields.setdefault('create', True)
    extra_fields.setdefault('mappings_json', dict(class_name="label", start_date="start_date", end_date="end_date"))

    user = get_user(user_full_name)

    driver_type = factory.get(mimetype)

    class_system = get_classification_system(classification_system_name, classification_system_version)

    _accessor = DBAccessor(system_id=class_system.id)

    try:
        dataset_data_table, field_seq = make_dataset_table(table_name=dataset_table_name, create=extra_fields['create'])
    except BaseException as err:
        drop_dataset_table(dataset_data_table, field_seq)
        raise RuntimeError('Error while create the dataset table data')

    try:
        driver: Driver = driver_type(entries=dataset_file,
                                     mappings=extra_fields['mappings_json'],
                                     storager=_accessor,
                                     user=user.id,
                                     system=class_system)

        driver.load_data_sets()

        driver.store(dataset_data_table)

        _db.session.commit()

        logging.info('Data inserted in table {}'.format(driver.__class__.__name__))

        affected_rows = len(driver.get_data_sets())
        return dataset_data_table, field_seq, affected_rows
    except BaseException as err:
        _db.session.rollback()
        drop_dataset_table(dataset_data_table, field_seq)
        raise RuntimeError('Error while insert the dataset table data')


def create_dataset(user_full_name, classification_system_name, classification_system_version, collect_method_name,
                   dataset_name, dataset_table_name, title, start_date, end_date, version, **extra_fields):
    """Insert a new dataset."""
    extra_fields.setdefault('description', "")
    extra_fields.setdefault('version_predecessor', None)
    extra_fields.setdefault('version_successor', None)
    extra_fields.setdefault('metadata_json', None)
    extra_fields.setdefault('is_public', True)

    user = get_user(user_full_name)

    classification_system = get_classification_system(classification_system_name, classification_system_version)

    collect_method = get_collect_method(collect_method_name)

    dataset_infos = dict(
        name=dataset_name,
        title=title,
        start_date=start_date,
        end_date=end_date,
        description=extra_fields["description"],
        version=version,
        version_predecessor=extra_fields["version_predecessor"],
        version_successor=extra_fields["version_successor"],
        is_public=extra_fields["is_public"],
        classification_system_id=classification_system.id,
        collect_method_id=collect_method.id,
        metadata_json=extra_fields['metadata_json'],
        dataset_table_name=dataset_table_name,
        user_id=user.id
    )

    with _db.session.begin_nested():
        ds = Datasets(**dict(dataset_infos))

        _db.session.add(ds)

    _db.session.commit()

    return dataset_infos


def delete_dataset_table(ds_name, ds_version):
    """Delete dataset table."""
    ds_sq = ds_name.replace("-", "_")

    s_name = f"{Config.SAMPLEDB_SCHEMA}.dataset_{ds_sq}_id_seq"

    ds_table = _db.session.query(Datasets).filter(
        and_(Datasets.name == ds_name,
             Datasets.version == ds_version)
    ).first_or_404()

    dataset_table_info = Table(ds_table.dataset_table_name, metadata, autoload=True, autoload_with=_db.engine,
                               extend_existing=True)

    with _db.session.begin_nested():
        _db.session.delete(ds_table)
        dataset_table_info.drop(bind=_db.engine)
        _db.session.execute(f"DROP SEQUENCE {s_name};")

    _db.session.commit()

    return
