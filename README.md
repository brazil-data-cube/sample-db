# sampledb

## Structure

- [`bdc_sample`](./bdc_sample) Python module for sampledb. It also includes script for data loading
- [`spec`](./spec) Contains sampledb specification, such SQL functions to prepare database and ERD diagram (`draw.io`)

## Installation

### Requirements

Make sure you have the following libraries installed:

- [`Python 3`](https://www.python.org/)
- [`gdal`](https://gdal.org/)
- [`postgresql`](https://www.postgresql.org/download/)
- [`postgis`](https://postgis.net/)
- [`geopandas`](http://geopandas.org/)
- [`R`](https://www.r-project.org/) (Required for [inSitu](https://github.com/e-sensing/inSitu) sample driver)

After that, install Python dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Running

We have prepared [`migration`](./migrations) config using [`alembic`](https://alembic.sqlalchemy.org/en/latest/).
Create database `sampledb` with the following command:

```psql
CREATE DATABASE sampledb TEMPLATE template1;
\c sampledb
CREATE EXTENSION postgis
```

After that, run migration command to prepare model tables:

```python
alembic upgrade head
```

Edit the file [`sample2db.py`](./examples/sample2db.py) with directory where sample is stored.

For example:

```python
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
    db.init_model('postgresql://postgres:postgres@localhost:5432/sampledb')

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
        Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager, user, luc_system),
        InSitu('/data/inSitu', storager, user, luc_system),
        Dpi('/data/Ieda/', storager, user, luc_system),
        Fototeca('/data/Rodrigo/Rodrigo-BareSoil', storager, user, luc_system)
    ]

    for driver in drivers:
        try:
            driver.load_data_sets()
            driver.store()
            print("Done {}".format(driver.__class__.__name__))
        except BaseException as err:
            print(err)
```

After that, execute the `sample2db.py`:

```bash
python sample2db.py
```

## Docker

You can use Docker environment to execute the script `sample2db.py`

Build docker image with the following command:

```bash
docker-compose build
```

Create PostgreSQL with PostGIS docker container with command:

```bash
docker-compose up -d db
docker-compose exec db \
                    psql -U postgres -c "CREATE DATABASE sampledb TEMPLATE template1"
docker-compose exec db \
                    psql -U postgres -d sampledb -c "CREATE EXTENSION postgis"
```

To create migration, make sure the database connection parameters is correct in `alembic.ini`. Run the following command to create migrations:

```bash
docker-compose run --rm \
                   -e SQLALCHEMY_URI=postgresql://postgres:postgres@bdc_pg/sampledb \
                   sampledb \
                   alembic upgrade head
```

After that, create container and execute the `sample2db.py` (**Make sure** that database connection parameters is correct. You can edit manually and mount as file in container):

```bash
docker-compose run --rm \
                   -e SQLALCHEMY_URI=postgresql://postgres:postgres@bdc_pg/sampledb \
                   --volume /data:/data \
                   sampledb \
                   python3 examples/sample2db.py
```