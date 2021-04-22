#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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
    'check-manifest>=0.40'
]


extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'tools': [
        'sample-db-utils @ git+https://github.com/brazil-data-cube/sample-db-utils.git@v0.6.0',
    ]
}

extras_require['all'] = [ req for exts, reqs in extras_require.items() for req in reqs ]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'sqlalchemy-views>=0.2.4',
    'GeoAlchemy2>=0.6.3',
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
    license='MIT',
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
        ]
    },
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
