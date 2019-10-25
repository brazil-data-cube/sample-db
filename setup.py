#!/usr/bin/env python

import os
from setuptools import find_packages, setup


tests_require = [
    'pytest>=5.0.0,<6.0.0',
]


extras_require = {
    "docs": [
        'bdc-readthedocs-theme @ git+git://github.com/brazil-data-cube/bdc-readthedocs-theme.git#egg=bdc-readthedocs-theme',
        'Sphinx>=2.1.2',
    ],
    "tests": tests_require
}

g = {}
with open(os.path.join('bdc_sample', 'manifest.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['version']

setup(
    name='bdc-sample',
    version=version,
    description='Brazilian Data Cube Sample package',
    author='Admin',
    author_email='admin@admin.com',
    url='https://github.com/brazil-data-cube/sampledb.git',
    packages=find_packages(),
    install_requires=[
        'geopandas>=0.5.0',
        'gdal>=2.3.3,<3',
        'SQLAlchemy[postgresql]>=1.3.4',
        'alembic>=1.0.10',
        'GeoAlchemy2>=0.6.3',
        'Shapely>=1.6.4',
        'Flask>=1.1.1',
        'Flask-Cors>=3.0.8',
        'flask-restplus>=0.13.0',
        'Flask-Script>=2.0.6',
        'flask_bcrypt>=0.7.1',
        'marshmallow-sqlalchemy>=0.19.0',
        'bdc-core @ git+git://github.com/brazil-data-cube/bdc-core.git#egg=bdc-core'
    ],
    extras_require=extras_require,
    tests_require=tests_require,
    include_package_data=True,
)
