from bdc_sample.models.base_sql import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Text


class LucClass(BaseModel):
    __tablename__ = 'luc_class'

    id = Column(Integer, primary_key=True)
    class_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    luc_classification_system_id = Column(Integer, ForeignKey('luc_classification_system.id', ondelete='NO ACTION'), nullable=False)
    parent_id = Column(Integer, ForeignKey('luc_class.id', ondelete='NO ACTION'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='NO ACTION'), nullable=False)