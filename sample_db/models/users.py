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

from bdc_db.sqltypes import JSONB
from lccs_db.models.base import BaseModel
from sqlalchemy import (Column, ForeignKey, Index, Integer,
                        PrimaryKeyConstraint, String)

from ..config import Config


class Users(BaseModel):
    """User Model."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False, unique=True)

    __table_args__ = (
        Index(None, email),
        Index(None, name),
        Index(None, institution),
        Index(None, user_id),
        dict(schema=Config.SAMPLEDB_SCHEMA),
    )