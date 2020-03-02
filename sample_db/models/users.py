#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB User Model."""

from sqlalchemy import Column, Integer, String

from sample_db.models.base import BaseModel

from ..config import Config

from werkzeug.security import generate_password_hash, check_password_hash

class Users(BaseModel):
    """User Model."""

    __tablename__ = 'users'
    __table_args__ = {'schema': Config.ACTIVITIES_SCHEMA}

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column('password', String, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, value):
        """
        Check password input value against a string and return true if match
        :param value: str
        :return: bool
        """
        return check_password_hash(self.password, value)
