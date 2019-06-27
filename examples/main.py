# Models
from bdc_sample.models import db, LucClassificationSystem, User
# Drivers
from bdc_sample.core.postgis_accessor import PostgisAccessor
from bdc_sample.drivers.embrapa import Embrapa
from bdc_sample.drivers.inSitu import InSitu
from bdc_sample.drivers.dpi import Dpi
from bdc_sample.drivers.fototeca import Fototeca



if __name__ == '__main__':
    # Initialize SQLAlchemy Models
    db.init_model('postgresql://postgres:postgres@localhost:5432/teste')
    # db.Model.metadata.create_all()

    users = db.session.query(User).filter(User.email == "admin@admin.com")

    if users.count() == 0:
        user = User(full_name="Admin", email="admin@admin.com")
        user.password = "admin"
        user.save()
    else:
        user = users[0]

    luc_systems = db.session.query(LucClassificationSystem).filter(LucClassificationSystem.system_name == "BDC")

    if luc_systems.count() == 0:
        luc_system = LucClassificationSystem(authority_name="Brazil Data Cube", system_name="BDC", description="", user_id=user.id)
        luc_system.save()
    else:
        luc_system = luc_systems[0]

    storager = PostgisAccessor()

    drivers = [
#        Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager, user, luc_system),
#        InSitu('/data/inSitu', storager, user, luc_system),
#        Dpi('/data/Ieda/', storager, user, luc_system),
        Fototeca('/data/Rodrigo/Rodrigo-BareSoil', storager, user, luc_system)
    ]

    for driver in drivers:
        try:
            driver.load_data_sets()
            driver.store()
            print("Done {}".format(driver.__class__.__name__))
        except BaseException as err:
            print(err)
