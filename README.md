# sampledb

## Structure

- [`bdc_sample`](./bdc_sample) Python module for sampledb. It also includes script for data loading
- [`spec`](./spec) Contains sampledb specification, such SQL functions to prepare database and ERD diagram (`draw.io`)

## Installation

### Requirements

Make sure you have the following libraries installed:

- [`gdal`](https://gdal.org/)
- [`postgresql`](https://www.postgresql.org/download/)
- [`postgis`](https://postgis.net/)

After that, install Python dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Running

We have prepared [`migration`](./migrations) config using [`alembic`](https://alembic.sqlalchemy.org/en/latest/).
Create database `sampledb` with the following command:

```psql
CREATE DATABASE sampledb TEMPLATE template1;
```

After that, edit database credentials `sqlalchemy.url` in `alembic.ini`. Once configured, run migration command to prepare model tables:

```python
alembic upgrade head
```

