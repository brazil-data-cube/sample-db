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
    sampledb | teste_observations | table | postgres
    sampledb | users              | table | postgres
    (5 rows)

.. note::

    For more information on ``sample-db`` commands, please, type in the command line::

        sample-db  --help