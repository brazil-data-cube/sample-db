..
    This file is part of Sample Database Model.
    Copyright (C) 2019-2020 INPE.

    Sample Database Model is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

.. _Installation:

Installation
============

``sample-db`` implementation depends essentially on `GeoAlchemy2 <https://geoalchemy-2.readthedocs.io/en/latest/>`_, `LCCS Database Module <https://github.com/brazil-data-cube/lccs-db>`_ and the `Sample Database Utils <https://github.com/brazil-data-cube/sample-db-utils>`_.


Production installation
-----------------------

**Under Development!**


Development installation
------------------------

Clone the software repository:

.. code-block:: shell

        $ git clone https://github.com/brazil-data-cube/sample-db.git


Go to the source code folder:

.. code-block:: shell

        $ cd sample-db


Install in development mode:

.. code-block:: shell

        $ pip3 install -e .[all]


Run the tests:

.. code-block:: shell

        $ ./run-tests.sh


Generate the documentation:

.. code-block:: shell

        $ python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under:

.. code-block:: shell

    docs/sphinx/_build/html/