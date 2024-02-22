..
    This file is part of SAMPLE-DB.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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

        python3.11 -m venv venv


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

    sphinx-build docs/sphinx docs/sphinx/_build/html


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html
