"""
Defines an implementation of VMaus's samples
"""

from bdc_sample.core.driver import CSV


class VMaus(CSV):
    """
    Driver for VMaus Sample for data loading to `sampledb`
    """
    def __init__(self, entries, mappings=None, **kwargs):
        """Builds a Fototeca driver"""

        if not mappings:
            mappings = dict(
                class_name='label',
                start_date='from',
                end_date='to'
            )

        super(VMaus, self).__init__(entries, mappings, **kwargs)
