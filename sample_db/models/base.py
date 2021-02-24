#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Base Model."""

from sqlalchemy import MetaData

from ..config import Config

metadata = MetaData(schema=Config.SAMPLEDB_SCHEMA_NAME)
