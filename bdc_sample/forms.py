"""Defines Marshmallow Forms for SampleDB abstractions"""

from marshmallow_sqlalchemy import ModelSchema
from bdc_sample.models import LucClassificationSystem


class LucClassificationSystemSchema(ModelSchema):
    """Marshmallow Forms for LucClassificationSystem"""

    class Meta:
        """Internal"""
        model = LucClassificationSystem
