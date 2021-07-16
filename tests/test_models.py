#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for extension SAMPLE-DB."""
import pytest
from shapely.geometry import Point
from geoalchemy2.shape import from_shape

from sample_db import BDCSample
from sample_db.models import Datasets, CollectMethod
from sample_db.models.dataset_table import DatasetType


def _prepare_samples_fields():
    features = [
        dict(class_id=1, geometry=from_shape(shape=Point(0, 0),  srid=4326)),
        dict(class_id=1, geometry=from_shape(shape=Point(0, 1), srid=4326)),
        dict(class_id=1, geometry=from_shape(shape=Point(1, 2), srid=4326))
    ]
    return dict(
        table_name='FakeSample',
        version="1",
        features=features
    )


def _prepare_ds_fields():
    return dict(
        user_id=1,
        classification_system_id=1,
        start_date='2007-01-01',
        end_date='2007-01-01',
        is_public=True,
        title='FakeSample'
    )


@pytest.fixture
def db(app):
    ext = BDCSample(app)

    yield ext.db


def test_create_collect(db):
    collect_method_infos = dict(name="test-collect", description='test-collect-description')

    with db.session.begin_nested():
        cl = CollectMethod(**collect_method_infos)

        db.session.add(cl)

    db.session.commit()

    assert cl and cl.name == collect_method_infos['name']


def test_create_ds_table(db):
    with db.session.begin_nested():
        dataset_type = DatasetType()
        dataset_type.create()

        ds = Datasets.create_ds_table(table_name='fake-sample',  version="1")
        ds.user_id = 1
        ds.classification_system_id = 1
        ds.start_date = '2007-01-01'
        ds.end_date = '2007-01-01'
        ds.is_public = True
        ds.collect_method_id = 1
        ds.title = 'Fake Sample'
        db.session.add(ds)
    db.session.commit()

    assert ds and ds.name == 'fake-sample'
    assert ds.ds_table is not None
