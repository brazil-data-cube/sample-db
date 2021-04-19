#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for extension SAMPLE-DB."""

from sample_db import BDCSample


def test_ext_creation(app):
    ext = BDCSample(app)

    assert app.extensions['sample-db'] == ext