..
    This file is part of Sample Database Model.
    Copyright (C) 2019-2020 INPE.

    Sample Database Model is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

.. _Installation:

Installation
============

``sample-db`` implementation depends essentially on

- `GeoAlchemy2 <https://geoalchemy-2.readthedocs.io/en/latest/>`_.
- `LCCS Database Module <https://github.com/brazil-data-cube/lccs-db>`_.
- `Sample Database Utils <https://github.com/brazil-data-cube/sample-db-utils>`_.

Development Installation - GitHub
---------------------------------

Clone the Software Repository
+++++++++++++++++++++++++++++

Use ``git`` to clone the software repository::

        git clone https://github.com/brazil-data-cube/sample-db.git


Install SAMPLE-DB in Development Mode
+++++++++++++++++++++++++++++++++++++

Go to the source code folder::

        cd sample-db


Install in development mode::

        pip3 install -e .[all]

.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Run the Tests
+++++++++++++

Run the tests::

    ./run-tests.sh


Build the Documentation
+++++++++++++++++++++++


You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html


Production Installation - GitHub
--------------------------------


Install from GitHub::

    pip3 install git+https://github.com/brazil-data-cube/sample-db
