..
    This file is part of SAMPLE-DB.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


========================================
Brazil Data Cube - Sample Database Model
========================================

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
        :target: https://github.com/brazil-data-cube/sample-db/blob/master/LICENSE
        :alt: Software License

.. image:: https://drone.dpi.inpe.br/api/badges/brazil-data-cube/sample-db/status.svg
        :target: https://drone.dpi.inpe.br/brazil-data-cube/sample-db
        :alt: Build Status

.. image:: https://codecov.io/gh/brazil-data-cube/sample-db/branch/master/graph/badge.svg?token=WIJ67G1AAO
        :target: https://codecov.io/gh/brazil-data-cube/sample-db
        :alt: Code Coverage Test

.. image:: https://readthedocs.org/projects/sample-db/badge/?version=latest
        :target: https://sample-db.readthedocs.io/en/latest/
        :alt: Documentation Status


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

Currently, several projects systematically provide information on the dynamics of land use and cover. Well known projects include PRODES, DETER and TerraClass. These projects are developed by INPE and they produce information on land use and coverage used by the Brazilian Government to make public policy decisions. Besides these projects there are other initiatives from universities and space agencies devoted to the creation of national and global maps.

These data products are generated using different approaches and methodologies. In this context, the data set used in the sample and validation plays a fundamental role in the classification algorithms that generate new land use and coverage maps. A classified map’s accuracy depends directly on the quality of the training samples used by the machine learning methods.

Land use and cover samples are collected by different projects and individuals, using different methods, such as in situ gathering in fieldwork and visual interpretation of high-resolution satellite images. An important requirement is to be able to describe samples with proper metadata that characterize their differences and organize them in a shared database to facilitate the reproducibility of experiments. It is also important to develop tools to easily discover, query, access, and process this shared sample database.

Sample-DB (Sample Database) provides a data model that represents the land use and cover samples collected by different projects and individuals.

The following diagram shows the tables used in this system:

.. image:: https://github.com/brazil-data-cube/sample-db/raw/master/docs/model/db-schema.png
        :target: https://github.com/brazil-data-cube/sample-db/tree/master/docs/model
        :width: 90%
        :alt: Database Schema

This package is related to other softwares in the Brazil Data Cube project:

- `SAMPLE-DB-UTILS <https://github.com/brazil-data-cube/sample-db-utils>`_: Utility Functions for the SAMPLE-DB.

- `SAMPLE.py <https://github.com/brazil-data-cube/sample.py>`_: Python Client Library for Sample-DB.

- `LCCS-DB <https://github.com/brazil-data-cube/lccs-db>`_: Land Cover Classification System Database Model.

- `LCCS-WS-SPEC <https://github.com/brazil-data-cube/lccs-ws-spec>`_: Land Cover Classification System Web Service specification.

- `LCCS-WS <https://github.com/brazil-data-cube/lccs-ws>`_: Land Cover Classification System Web Service implementation.

- `LCCS.py <https://github.com/brazil-data-cube/lccs.py>`_: Python Client Library for Land Cover Classification System Web Service.

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
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.