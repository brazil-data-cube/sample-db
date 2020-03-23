#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Base Model."""

from ..config import Config

from sqlalchemy import MetaData


metadata = MetaData(schema=Config.ACTIVITIES_SCHEMA)