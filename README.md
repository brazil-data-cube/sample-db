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

Edit the file `main.py` with directory where sample is stored.

For example:

```python
from bdc_sample.postgisAccessor import PostgisAccessor
from bdc_sample.drivers.embrapa import Embrapa
from bdc_sample.drivers.inSitu import InSitu
from bdc_sample.drivers.dpi import Dpi

# PostGIS handler where data will be stored
storager = PostgisAccessor(host='localhost', username='postgres', password='postgres', database='sample')
# Driver for Embrapa sample
embrapa = Embrapa('/data/Embrapa/Pontos_Coletados_Embrapa', storager=storager)
embrapa.load_data_sets()
embrapa.store()
# Driver for InSitu sample
inSitu = InSitu('/data/inSitu', storager=storager)
inSitu.load_data_sets()
inSitu.store()
# Driver for DPI Sample
dpi = Dpi('/data/Ieda/', storager=storager)
dpi.load_data_sets()
dpi.store()
```

After that, execute the `main.py`:

```bash
python main.py
```