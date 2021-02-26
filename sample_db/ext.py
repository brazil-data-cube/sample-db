#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Sample extension for Brazil Data Cube applications and services."""

from bdc_db.ext import BrazilDataCubeDB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .cli import cli
from bdc_db.db import db as _db


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
            Make sure to initialize the `BDCCatalog` before.
        """
        return _db