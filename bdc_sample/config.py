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
    SQLALCHEMY_URI = os.environ.get('SQLALCHEMY_URI', 'postgresql://postgres:postgres@localhost/sampledb')
    CLIENT_SECRET_KEY = 'CHANGE_ME'
    CLIENT_AUDIENCE = 'samples'


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