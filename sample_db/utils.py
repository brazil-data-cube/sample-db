#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils Interface for the Sample Database Model ."""
from bdc_db.db import db as _db
from lccs_db.models import LucClassificationSystem
from sample_db_utils.core.driver import Driver
from sample_db_utils.core.postgis_accessor import PostgisAccessor
from sqlalchemy.orm.exc import NoResultFound

from .models import CollectMethod, Datasets, Users, make_dataset_table


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
                         classification_system_version, driver_type, **kwargs):
    """Insert dataset data into database."""
    user = get_user(user_full_name)

    class_system = get_classification_system(classification_system_name, classification_system_version)

    observation_table = make_dataset_table(table_name=dataset_table_name, create=kwargs['obs_already_exist'])

    _accessor = PostgisAccessor(system_id=class_system.id)

    driver: Driver = driver_type(entries=kwargs['dataset_file'],
                                 mappings=kwargs['mappings_json'],
                                 storager=_accessor,
                                 user=user.id,
                                 system=class_system)
    _db.session.commit()

    try:
        driver.load_data_sets()
        driver.store(observation_table)
        print('Data inserted in table {}'.format(driver.__class__.__name__))
    except BaseException as err:
        _db.session.rollback()
        print(err)

    affected_rows = len(driver.get_data_sets())

    return affected_rows


def create_dataset(user_full_name, classification_system_name, classification_system_version, collect_method_name,
                   dataset_table_name, **kwargs):
    """Insert a new dataset."""
    user = get_user(user_full_name)

    class_system = get_classification_system(classification_system_name, classification_system_version)

    collect_method = get_collect_method(collect_method_name)

    dataset_table_full_name = f"dataset_{dataset_table_name}"

    kwargs["classification_system_id"] = class_system.id
    kwargs["user_id"] = user.id
    kwargs["collect_method_id"] = collect_method.id
    kwargs["dataset_table_name"] = dataset_table_full_name

    dataset = Datasets(**kwargs)

    try:
        with _db.session.begin_nested():
            _db.session.add(dataset)
        _db.session.commit()
    except Exception as e:
        _db.session.rollback()
        raise e
