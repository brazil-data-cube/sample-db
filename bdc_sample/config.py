"""
Brazil Data Cube Configuration
You can define these configurations and call using environment variable
`ENVIRONMENT`. For example: `export ENVIRONMENT=ProductionConfig`
"""

# pylint: disable=too-few-public-methods

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    return CONFIG.get(env)


class Config():
    DEBUG = False
    TESTING = False

    AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY', 'bdc#2019key')
    ALGORITHM = os.environ.get('ALGORITHM', 'RS256')
    EXPIRES_IN_AUTH = int(os.environ.get('EXPIRES_IN_AUTH', '3600'))
    EXPIRES_IN_CLIENT = int(os.environ.get('EXPIRES_IN_CLIENT', '86400'))

    SQLALCHEMY_URI = os.environ.get('SQLALCHEMY_URI', 'postgresql://postgres:postgres@localhost/sampledb')


class ProductionConfig(Config):
    """Production Mode"""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development Mode"""
    DEVELOPMENT = True

class TestingConfig(Config):
    """Testing Mode (Continous Integration)"""
    TESTING = True
    DEBUG = True


CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}