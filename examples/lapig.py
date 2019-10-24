"""
Defines an implementation of Lapig's drivers
"""

from bdc_sample.core.driver import CSV


class Lapig(CSV):
    """
    Driver for Lapig Sample for data loading to `sampledb`
    """
    def __init__(self, entries, mappings=None, **kwargs):
        """Builds a Fototeca driver"""

        if not mappings:
            mappings = dict(class_name='label')

        super(Lapig, self).__init__(entries, mappings, **kwargs)
