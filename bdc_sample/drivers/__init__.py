"""List of Brazil Data Cube drivers"""

from bdc_sample.drivers.canasat import Canasat
from bdc_sample.drivers.cerrado import Cerrado
from bdc_sample.drivers.dpi import Dpi
from bdc_sample.drivers.embrapa import Embrapa
from bdc_sample.drivers.fototeca import Fototeca
from bdc_sample.drivers.inSitu import InSitu
from bdc_sample.drivers.lapig import Lapig
from bdc_sample.drivers.vmaus import VMaus


__all__ = [
    'Canasat',
    'Cerrado',
    'Dpi',
    'Embrapa',
    'Fototeca',
    'InSitu',
    'Lapig',
    'VMaus'
]