#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='bdc_sample',
    version='1.0',
    description='Brazilian Data Cube Sample package',
    author='Admin',
    author_email='admin@admin.com',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=find_packages(),
    include_package_data=True,
)
