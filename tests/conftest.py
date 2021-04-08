#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Config test fixtures."""

import subprocess

import pytest
from flask import Flask


@pytest.fixture
def app():
    """Flask application fixture."""
    app = Flask(__name__)

    return app


def pytest_sessionstart(session):
    """Load LCCS-DB and prepare database environment."""
    for command in ['init', 'create-namespaces', 'create-schema', 'load-scripts', 'create-extension-postgis']:
        subprocess.call(f'sample-db db {command}', shell=True)


def pytest_sessionfinish(session, exitstatus):
    """Destroy database created."""
    subprocess.call(f'sample-db db destroy --force', shell=True)
