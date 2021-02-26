#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils Interface for the Sample Database Model ."""
from sqlalchemy.orm.exc import NoResultFound
from bdc_db.db import db as _db
from sample_db_utils.core.postgis_accessor import PostgisAccessor
from sample_db_utils.core.driver import Driver
from lccs_db.models import LucClassificationSystem

from .models import make_observation, Users, Datasets, CollectMethod


def create_dataset(user_full_name, observation_table_name, classification_system_name, classification_system_version,
                   driver_type, **kwargs):
    """Utility function to create dataset."""
    
    accessor = PostgisAccessor()

    try:
        user = _db.session.query(Users)\
            .filter_by(full_name=user_full_name)\
            .one()
    except NoResultFound:
        raise RuntimeError(f'User {user_full_name} not found!')

    try:
        class_system = _db.session.query(LucClassificationSystem)\
            .filter_by(name=classification_system_name, version=classification_system_version)\
            .one()
    except NoResultFound:
        raise RuntimeError(f'Classification System {classification_system_name} not found!')
    
    print(observation_table_name)

    observation_table = make_observation(table_name=observation_table_name, create=kwargs['obs_already_exist'])
    
    print(driver_type)

    driver: Driver = driver_type(entries=kwargs['observation_file'],
                                 mappings=kwargs['mappings_json'],
                                 storager=accessor,
                                 user=user.id,
                                 system=class_system)
    print(observation_table.name)

    _db.session.commit()

    try:
        driver.load_data_sets()
        driver.store(observation_table)
        print('Observation table insert {}'.format(driver.__class__.__name__))
    except BaseException as err:
        print(err)

    affected_rows = len(driver.get_data_sets())

    # try:
    #     collect_method = CollectMethod.get(name=kwargs['collect_method'])
    # except ValueError:
    #     raise RuntimeError(f'Collect Method {kwargs["collect_method"]} not found!')
    #
    # obs_table_name = driver.__class__.__name__

    _db.session.commit()
    
    return affected_rows

