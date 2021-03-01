..
    This file is part of Sample Database.
    Copyright (C) 2020-2021 INPE.

    Sample Database Module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


==================================
Brazil Data Cube - Sample Database
==================================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/sample-db/blob/master/LICENSE
        :alt: Software License

.. image:: https://readthedocs.org/projects/sample-db/badge/?version=latest
        :target: https://sample-db.readthedocs.io/en/latest/
        :alt: Documentation Status

.. image:: https://drone.dpi.inpe.br/api/badges/brazil-data-cube/sample-db/status.svg
        :target: https://drone.dpi.inpe.br/brazil-data-cube/sample-db
        :alt: Build Status

.. image:: https://codecov.io/gh/brazil-data-cube/sample-db/branch/master/graph/badge.svg?token=WIJ67G1AAO
        :target: https://codecov.io/gh/brazil-data-cube/sample-db
        :alt: Code Coverage Test

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/tag/brazil-data-cube/sample-db.svg
        :target: https://github.com/brazil-data-cube/sample-db/releases
        :alt: Release

.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord

About
=====

This is the storage module for data samples from the Brazil Data Cube. The module relies on SQLAlchemy related packages in order to store and retrieve data items related to the samples. All the sample collections are recorded in tables according to the following schema:

.. image:: https://github.com/brazil-data-cube/sample-db/raw/master/docs/model/db-schema.png
        :target: https://github.com/brazil-data-cube/sample-db/tree/master/docs/model
        :width: 90%
        :alt: Database Schema


Installation
============

Install from GitHub::

    pip3 install git+https://github.com/brazil-data-cube/sample-db

Documentation
=============

See https://sample-db.readthedocs.io/en/latest/

License
=======

.. admonition::
    Copyright (C) 2020-2021 INPE.

    Brazil Data Cube Sample Database Module is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.