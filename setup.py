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
"""Sample-db setup."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
    'docutils>=0.10,<0.15'
]

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'sqlalchemy-diff>=0.1.3',
    'alembic-verify>=0.1.4',
    'check-manifest>=0.40',
    'shapely>=1.7,<2',
]

sample_requires = [
    'sample-db-utils @ git+https://github.com/brazil-data-cube/sample-db-utils.git@v0.9.0',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'sample-utils': sample_requires,
}

extras_require['all'] = [ req for exts, reqs in extras_require.items() for req in reqs ]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'lccs-db @ git+https://github.com/brazil-data-cube/lccs-db.git@v0.8.2',
    'GeoAlchemy2>=0.6.3',
    'sqlalchemy-views>=0.2.4',
]

packages = find_packages()
with open(os.path.join('sample_db', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='sample_db',
    version=version,
    description=__doc__,
    keywords=['Land Use Land Cover', 'GIS', 'Database', 'Model', 'Samples'],
    license='GPLv3',
    author='Brazil Data Cube Team',
    author_email='brazildatacube@inpe.br',
    url='https://github.com/brazil-data-cube/sample-db',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'sample-db = sample_db.cli:cli',
        ],
        'bdc_db.alembic': [
            'sample-db = sample_db:alembic'
        ],
        'bdc_db.models': [
            'sample-db = sample_db.models'
        ],
        'bdc_db.triggers': [
            'sample-db = sample_db.triggers'
        ],
        'bdc_db.scripts': [
            'sample-db = sample_db.scripts'
        ],
        'bdc_db.namespaces': [
            'sample-db = sample_db.config:Config.SAMPLEDB_SCHEMA'
        ],
        'bdc.schemas':[
            'sample-db = sample_db.jsonschemas'
        ]
    },
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPL v3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
