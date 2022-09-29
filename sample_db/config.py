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
"""Define config file for Brazil Data Cube Sample Database Model."""

import os

CURRENT_DIR = os.path.dirname(__file__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Define common config along contexts."""

    SAMPLEDB_SCHEMA = os.environ.get('SAMPLEDB_SCHEMA', 'sampledb')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                        'postgresql://postgres:postgres@localhost:5432/sample')
