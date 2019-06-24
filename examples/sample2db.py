from bdc_sample.postgisAccessor import PostgisAccessor
from bdc_sample.drivers.embrapa import Embrapa
from bdc_sample.drivers.inSitu import InSitu
from bdc_sample.drivers.dpi import Dpi
from bdc_sample.drivers.fototeca import Fototeca


if __name__ == '__main__':
    storager = PostgisAccessor(host='localhost', username='postgres', password='postgres', database='amostras')

    # TODO: Retrieve from database. Enable to create new one
    # User Identifier
    user = 1
    # Classification System Identifier
    system = 1

    drivers = [
        Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager, user, system),
        InSitu('/data/inSitu', storager, user, system),
        Dpi('/data/Ieda/', storager, user, system),
        Fototeca('/data/Rodrigo/Rodrigo-BareSoil', storager, user, system)
    ]

    for driver in drivers:
        driver.load_data_sets()
        driver.store()