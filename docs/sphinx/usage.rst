..
    This file is part of Sample Database Model.
    Copyright (C) 2020-2020 INPE.

    Sample Database Model is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Usage
=====

Running SAMPLE-DB in the Command Line
-------------------------------------


If you have not installed ``sample-db`` yet, please, take a look at the :ref:`Installation Guide <Installation>`.

Creating a PostgreSQL Database
++++++++++++++++++++++++++++++

If you do not have a database instance, you can create one with the command line utility ``sample-db``::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db init

Create a schema (or namespace) named "``sampledb``" in this database::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db create-namespaces

You can see all namespaces::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db show-namespaces


Enable the ``PostGIS`` extension::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db create-extension-postgis


Creating the Sample Data Model
++++++++++++++++++++++++++++++

The command line utility ``sample-db`` can also be used to create all tables belonging to the Sample Data Model. The following command can be used to create or upgrade the table schema for SAMPLE-DB::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db alembic upgrade

If the above command succeed, you can check the created tables within the ``sample-db`` schema in PostgreSQL. Use the ``psql`` terminal as follow::

    psql -U username -h host -p 5432 -d dbname -c "\dt sampledb.*"


You should get a similar output::

                  List of relations
      Schema  |        Name        | Type  |  Owner
    ----------+--------------------+-------+----------
    sampledb | collect_method     | table | postgres
    sampledb | datasets           | table | postgres
    sampledb | provenance         | table | postgres
    (3 rows)


Setting up PL/pgSQL Triggers and Loading default script data
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You can show the triggers loaded using the command line::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db show-triggers

To register them into the database system, use the command::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db create-triggers

You can load well-known classification systems with the CLI::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample-db db load-scripts


Insert data into Sample
+++++++++++++++++++++++


To create a new dataset, you must first enter the data that contains the geometry and classes of the samples. To do this, run the command below. One of the parameters to be informed is the path to the data that you want to store in the database ::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname"  \
    sample-db sample insert-dataset-table \
    --user_id 1 \
    --dataset_table_name bdc_cerrado \
    --mappings /path/to/mapping/mapping.json \
    --classification_system_name BDC \
    --classification_system_version 1 \
    --dataset_file /path/to/observation.zip --verbose

You should get a similar output::

                  List of relations
      Schema  |        Name        | Type  |  Owner
    ----------+--------------------+-------+----------
     sampledb | dataset_bdc_cerrado| table | postgres
     sampledb | collect_method     | table | postgres
     sampledb | datasets           | table | postgres
     sampledb | provenance         | table | postgres
    (4 rows)


Create a dataset::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname"  \
    sample-db sample create-dataset \
    --user_id 1 \
    --dataset_table_name bdc_cerrado \
    --name sample-cerrado-2017_2018 \
    --title BDC-Dados-Cerrado-2017-2018 \
    --start_date 2017-06-01 \
    --end_date 2018-06-30 \
    --version 1 \
    --no-public \
    --collect_method Visual \
    --description This is a description of the dataset \
    --classification_system_name PRODES \
    --classification_system_version 1.0 \
    --metadata_file /path/to/metadata/sample-metadata.json --verbose

To create a view of ``dataset_table``, run the commannd::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname"  \
    sample-db sample create-view-dataset-table \
    --dataset_table_name bdc_cerrado

.. note::

    For more information on ``sample-db`` commands, please, type in the command line::

        sample-db  --help