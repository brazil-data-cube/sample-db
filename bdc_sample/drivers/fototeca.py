"""
Defines an implementation of Fototeca's drivers
"""

from bdc_sample.core.driver import CSV


class Fototeca(CSV):
    """
    Driver for Fototeca Sample for data loading to `sampledb`

    By default, the Fototeca samples mappings contains the following structure:
        - label Sample class name
        - start_date Sample start date
        - end_date Sample end date
        - latitude
        - longitude
    """

    def __init__(self, entries, mappings=None, **kwargs):
        """Builds a Fototeca driver"""

        if not mappings:
            mappings = dict(class_name='label')

        super(Fototeca, self).__init__(entries, mappings, **kwargs)
