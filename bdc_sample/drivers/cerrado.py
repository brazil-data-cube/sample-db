"""
Samples Cerrado
"""

from re import search as regex_search
from datetime import datetime
from os import path
from bdc_sample.core.driver import Shapefile


class Cerrado(Shapefile):
    """Driver for Cerrado Sample for data loading to `sampledb`"""

    def __init__(self, entries, **kwargs):
        mappings = dict(class_name='CLASSE PRI')

        super(Cerrado, self).__init__(entries, mappings, **kwargs)

    def load(self, file):
        file_name = path.splitext(path.basename(file))[0]

        matched = regex_search(r'.*?(\d+)$', file_name)

        if matched.group(1):
            year = int(matched.group(1))

            self.mappings['start_date'].setdefault(
                'value',
                datetime(year=year, month=1, day=1))

            self.mappings['end_date'].setdefault(
                'value',
                datetime(year=year, month=12, day=31))
        else:
            now = datetime.utcnow()
            self.mappings['start_date'].setdefault('value', now)
            self.mappings['end_date'].setdefault('value', now)

        return super(Cerrado, self).load(file)
