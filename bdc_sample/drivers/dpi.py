from datetime import datetime
from shapely.geometry import Point
from bdc_sample.core.driver import Shapefile
from bdc_sample.core.utils import reproject


class Dpi(Shapefile):
    """Driver for data loading to `sampledb`"""

    def __init__(self, entries, **kwargs):
        mappings = dict(
            class_name="ext_na",
            start_date=dict(value='2015-10-01'),
            end_date=dict(value='2016-07-31')
        )

        super(Dpi, self).__init__(entries, mappings, **kwargs)