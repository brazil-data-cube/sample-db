#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Define config file for Brazil Data Cube Sample Database Model."""

import os
import tempfile

CURRENT_DIR = os.path.dirname(__file__)


def get_settings(env):
    """Retrieve respective config context."""
    return CONFIG.get(env)


class Config:
    """Define common config along contexts."""

    DEBUG = False
    TESTING = False
    ACTIVITIES_SCHEMA = os.environ.get('ACTIVITIES_SCHEMA', 'sampledb')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://postgres:123456@localhost:5432/sampledb'
    )

class ProductionConfig(Config):
    """Production Mode."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Development Mode."""

    DEVELOPMENT = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)."""

    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}