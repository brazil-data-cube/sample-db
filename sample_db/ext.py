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

"""Sample extension for Brazil Data Cube applications and services."""
from bdc_db.db import db as _db
from bdc_db.ext import BrazilDataCubeDB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .cli import cli


class BDCSample:
    """Image sample extension."""

    # Reference to BrazilDataCubeDB app instance
    _db_ext = None

    def __init__(self, app=None):
        """Initialize the sample_db extension.

        Args:
            app: Flask application
            kwargs: Optional arguments (not used).
        """
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize Flask application instance.

        Args:
            app: Flask application
            kwargs: Optional arguments (not used).
        """
        self._db_ext = BrazilDataCubeDB(app)
        app.extensions['sample-db'] = self

        app.cli.add_command(cli)

    @property
    def db(self) -> SQLAlchemy:
        """Retrieve instance Flask-SQLALchemy instance.

        Notes:
            Make sure to initialize the `BDCSample` before.
        """
        return _db