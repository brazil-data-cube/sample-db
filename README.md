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

We have prepared [`ddl-sample`](./spec/ddl-samples.sql) SQL file to create table, schema and functions structure.
Create database `sample` with the following command:

```psql
CREATE DATABASE sample TEMPLATE template1;
```

After that, execute the `ddl-sample.sql` file within context of `sample`.

Edit the file [`sample2db.py`](./examples/sample2db.py) with directory where sample is stored.

For example:

```python
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
```

After that, execute the `sample2db.py`:

```bash
python sample2db.py
```

## Docker

You can use Docker environment to execute the script `sample2db.py`

Build docker image with the following command:

```bash
docker build --tag bdc/sampledb -f docker/Dockerfile .
```

After that, create container and execute the `sample2db.py` (**Make sure** that database connection parameters is correct):

```bash
docker run -it --rm --name sampledb -v /path/to/the/sample_data:/data bdc/sample python examples/sample2db.py
```