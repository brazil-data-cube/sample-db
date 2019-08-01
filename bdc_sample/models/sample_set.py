from bdc_sample.models.base_sql import BaseModel
from geoalchemy2 import Geometry
from sqlalchemy import Column,ForeignKey, Integer, String, Text


class SampleSet(BaseModel):
    __tablename__ = 'saple_set'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    luc_classification_system_id = Column(Integer, ForeignKey('luc_classification_system.id', ondelete='NO ACTION'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='NO ACTION'), nullable=False)