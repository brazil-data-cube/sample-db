import os
import sys

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../'))

#pylint: disable=wrong-import-position

from bdc_sample.core.postgis_accessor import PostgisAccessor
from bdc_sample.models import db, LucClassificationSystem, User
from examples.canasat import Canasat
from examples.cerrado import Cerrado
from examples.sample_ieda import Dpi
from examples.embrapa import Embrapa
from examples.fototeca import Fototeca
from examples.inSitu import InSitu
from examples.lapig import Lapig
from examples.vmaus import VMaus


storager = PostgisAccessor()
class_systems = [
    {
        'authority_name': 'claudio',
        'system_name': 'Claudio',
        'description': 'Claudio\'s sample of Mission Points of Cerrado',
        'sample': [
            Cerrado('/data/Claudio/Pontos_Missoes_Cerrado', storager=storager)
        ]
    },
    {
        'authority_name': 'vmaus',
        'system_name': 'vmaus',
        'description': 'Victor Maus\'s sample',
        'sample': [
            VMaus('/data/Victor_Maus-Forest/samples_Victor.csv', storager=storager)
        ]
    },
    {
        'authority_name': 'Canasat',
        'system_name': 'Canasat',
        'description': 'Canasat\'s Pasture sample',
        'sample': [
            Canasat('/data/Canasat', storager=storager)
        ]
    },
    {
        'authority_name': 'lapig',
        'system_name': 'Lapig',
        'description': 'Lapig\'s Pasture sample',
        'sample': [
            Lapig('/data/Lapig-Pastagem', storager=storager)
        ]
    },
    {
        'authority_name': 'Ieda',
        'system_name': 'Ieda',
        'description': 'Ieda\'s sample',
        'sample': [
            Dpi('/data/Ieda/', storager=storager),
        ]
    },
    {
        'authority_name': 'Embrapa',
        'system_name': 'Embrapa',
        'description': 'Embrapa\'s sample',
        'sample': [
            Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager=storager),
        ]
    },
    {
        'authority_name': 'Rodrigo',
        'system_name': 'Rodrigo',
        'description': 'Fototeca\'s sample',
        'sample': [
            Fototeca('/data/Rodrigo/BareSoil', storager=storager),
            Fototeca('/data/Rodrigo/Cerrado-Campestre-Toposerra-Arboreo',
                     storager=storager),
            Fototeca('/data/Rodrigo/ClearCut', storager=storager),
            Fototeca('/data/Rodrigo/Eucalyptus', storager=storager),
            Fototeca('/data/Rodrigo/ForestDegradation', storager=storager),
            Fototeca('/data/Rodrigo/ForestFireScar', storager=storager),
            Fototeca('/data/Rodrigo/OilPalm', storager=storager),
            Fototeca('/data/Rodrigo/UrbanAreas', storager=storager),
        ]
    },
    {
        'authority_name': 'insitu',
        'system_name': 'InSitu',
        'description': 'InSitu\'s sample in R',
        'sample': [
            InSitu('/data/inSitu', storager=storager)
        ]
    }
]


if __name__ == '__main__':
    # Initialize SQLAlchemy Models
    uri = os.environ.get(
        'SQLALCHEMY_URI',
        'postgresql://postgres:postgres@localhost:5434/amostras')
    db.init_model(uri)

    try:
        user = User.get(email='admin@admin.com')
    except BaseException:
        user = User(full_name='Admin', email='admin@admin.com')
        user.password = 'admin'
        user.save()

    for class_system in class_systems:
        try:
            luc_system = LucClassificationSystem.get(
                system_name=class_system['system_name'])
        except BaseException:
            luc_system = LucClassificationSystem(user_id=user.id)
            luc_system.authority_name = class_system['authority_name']
            luc_system.description = class_system['description']
            luc_system.system_name = class_system['system_name']
            luc_system.save()

        for driver in class_system['sample']:
            try:
                driver.user = user
                driver.system = luc_system

                driver.load_data_sets()
                driver.store()
                print('Done {}'.format(driver.__class__.__name__))
            except BaseException as err:
                print(err)
