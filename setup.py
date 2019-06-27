#!/usr/bin/env python

from distutils.core import setup

setup(
    name='bdc_sample',
    version='1.0',
    description='Brazilian Data Cube Sample package',
    author='Admin',
    author_email='admin@admin.com',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=['bdc_sample', 'bdc_sample.core', 'bdc_sample.drivers', 'bdc_sample.models'],
    package_data={'': ['*.md']}
    # data_files=[('README.md'), ['README.md']]
)
