from bdc_sample.models.base_sql import BaseModel
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column('password', String, nullable=False)

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