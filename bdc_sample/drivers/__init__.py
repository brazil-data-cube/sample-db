"""List of Brazil Data Cube drivers"""

from bdc_sample.core.driver import CSV
from bdc_sample.core.driver import Shapefile
from bdc_sample.drivers.canasat import Canasat
from bdc_sample.drivers.cerrado import Cerrado
from bdc_sample.drivers.dpi import Dpi
from bdc_sample.drivers.embrapa import Embrapa
from bdc_sample.drivers.fototeca import Fototeca
from bdc_sample.drivers.inSitu import InSitu
from bdc_sample.drivers.lapig import Lapig
from bdc_sample.drivers.vmaus import VMaus


class DriverFactory:
    drivers = {
        'text/csv': CSV,
        'application/vnd.ms-excel': CSV,
        'application/zip': Shapefile,
        'application/x-zip-compressed': Shapefile
    }

    def add(self, driver_name, driver):
        self.drivers[driver_name] = driver

    def get(self, driver_name):
        assert driver_name in self.drivers

        return self.drivers[driver_name]


factory = DriverFactory()

__all__ = [
    'factory',
    'Canasat',
    'Cerrado',
    'Dpi',
    'Embrapa',
    'Fototeca',
    'InSitu',
    'Lapig',
    'VMaus'
]
