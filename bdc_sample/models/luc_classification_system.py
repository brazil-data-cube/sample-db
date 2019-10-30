from bdc_sample.models.base_sql import BaseModel
from sqlalchemy import Column, Integer, Text


class LucClassificationSystem(BaseModel):
    __tablename__ = 'luc_classification_system'

    id = Column(Integer, primary_key=True)
    authority_name = Column(Text, nullable=False)
    system_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)