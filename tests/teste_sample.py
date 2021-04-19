#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for sample-db."""

import subprocess
import sys

from click.testing import CliRunner

import pytest
from sample_db.cli import cli
from sample_db import BDCSample


def test_basic_cli():
    """Test basic cli usage."""
    res = CliRunner().invoke(cli)

    assert res.exit_code == 0


def test_cli_module():
    """Test the sample-db invoked as a module."""
    res = subprocess.call(f'{sys.executable} -m sample_db', shell=True)

    assert res == 0
