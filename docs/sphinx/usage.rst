..
    This file is part of Sample Database Model.
    Copyright (C) 2019-2020 INPE.

    Sample Database Model is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Usage
=====


Running SAMPLE-DB in the Command Line
-------------------------------------


If you have not installed ``sample-db`` yet, please, take a look at the :ref:`Installation Guide <Installation>`.

Creating a PostgreSQL Database
++++++++++++++++++++++++++++++

Create database instance, namespaces (schemas) and PostGIS extension with the command line utility ``sample_db``::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample_db init-db

The command line utility sample_db can also be used to create all tables belonging to the SAMPLE data model. The following command can be used to create or upgrade the table schema for SAMPLE::

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample_db alembic upgrade 03d259000eac

    SQLALCHEMY_DATABASE_URI="postgresql://username:password@host:5432/dbname" \
    sample_db alembic upgrade
