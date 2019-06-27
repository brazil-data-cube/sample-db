from datetime import datetime
from sqlalchemy import create_engine, Column, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class DatabaseWrapper(object):
    def __init__(self):
        maker = sessionmaker()
        self.DBSession = scoped_session(maker)
        self.session = None
        self.Model = declarative_base(metadata=MetaData(schema="bdc"))

    def init_model(self, uri):
        engine = create_engine(uri)
        self.DBSession.configure(bind=engine)
        self.session = self.DBSession()


db = DatabaseWrapper()

class DBO():
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

class BaseModel(db.Model, DBO):
    """
    Abstract class for ORM model.
    Injects both `created_at` and `updated_at` fields in table
    """
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())