from bdc_sample.models.base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Text


class LucClassificationSystem(BaseModel):
    __tablename__ = 'luc_classification_system'

    id = Column(Integer, primary_key=True)
    authority_name = Column(Text, nullable=False)
    system_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='NO ACTION'), nullable=False)