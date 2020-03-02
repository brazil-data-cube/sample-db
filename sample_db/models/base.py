#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Base Model."""

from datetime import datetime
from sqlalchemy import create_engine, Column, DateTime, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from ..config import Config

class DatabaseWrapper(object):
    def __init__(self):
        maker = sessionmaker()
        self.DBSession = scoped_session(maker)
        self.session = None
        self.Model = declarative_base(metadata=MetaData(schema=Config.ACTIVITIES_SCHEMA))

    def init_model(self, uri):
        self.engine = create_engine(uri)
        self.DBSession.configure(bind=self.engine)
        self.session = self.DBSession()


db = DatabaseWrapper()


class BaseModel(db.Model):
    """
    Abstract class for ORM model.
    Injects both `created_at` and `updated_at` fields in table
    """
    __abstract__ = True

    user_id = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(),
                                  onupdate=datetime.utcnow())

    def save(self, commit=True):
        """
        Save and persists object in database
        """

        db.session.add(self)

        if not commit:
            return

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Delete object from database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def _filter(cls, **properties):
        """Filter abstraction"""
        return db.session.query(cls).filter_by(**properties)

    @classmethod
    def filter(cls, **properties):
        """
        Filter data set rows following the provided restrictions
        Provides a wrapper of SQLAlchemy session query.
        Args:
            **properties (dict) - List of properties to filter of.
        Returns:
            list of BaseModel item Retrieves the filtered rows
        """
        return cls._filter(**properties).all()

    @classmethod
    def get(cls, **restrictions):
        """
        Get one data set from database.
        Throws exception **NoResultFound** when the filter
        does not match any result.
        Args:
            **properties (dict) - List of properties to filter of.
        Returns:
            BaseModel Retrieves the base model instance
        """
        return cls._filter(**restrictions).one()