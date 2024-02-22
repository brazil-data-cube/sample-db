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
Changes
=======

Version 1.0.0 (2024-02-22)
--------------------------

- Added users table (`#96 <https://github.com/brazil-data-cube/sample-db/issues/96>`_).
- Bug fix: Fixed error in dataset validation sqlalchemy.inspect is not valid (`#97 <https://github.com/brazil-data-cube/sample-db/issues/97>`_).
- Bug fix: Fixed problem with multiple connections when opening the dataset table retrieval function (`#98 <https://github.com/brazil-data-cube/sample-db/issues/98>`_).
- Updated the lccs-db version (`#102 <https://github.com/brazil-data-cube/sample-db/issues/102>`_).

Version 0.9.1 (2022-11-16)
--------------------------

- Change LICENSE to GPL v3 (`#91 <https://github.com/brazil-data-cube/sample-db/issues/91>`_).


Version 0.9.0 (2022-08-03)
--------------------------

- Add support for new version of LCCS-DB: (`#87 <https://github.com/brazil-data-cube/sample-db/issues/87>`_).

- Adding dataset metadata validation schema :(`#84 <https://github.com/brazil-data-cube/sample-db/issues/84>`_).

- Add support latest sample-db-utils (v0.9.0): (`#88 <https://github.com/brazil-data-cube/sample-db/issues/88>`_).

- Fixing ArgumentError: dialect.has_table in make_dataset_table.


Version 0.8.3 (2022-01-06)
--------------------------

- Bug fix: Error while get_ds_table when it has a capital letter (`#81 <https://github.com/brazil-data-cube/sample-db/issues/81>`_).


Version 0.8.2 (2021-11-05)
--------------------------

- Bug fix: Migration column "created_at" of relation "dataset_type" already exists (`#78 <https://github.com/brazil-data-cube/sample-db/issues/78>`_).


Version 0.8.1 (2021-10-06)
--------------------------

- Bug fix: Adding missing attribute in dataset type (`#75 <https://github.com/brazil-data-cube/sample-db/issues/75>`_).


Version 0.8.0 (2021-08-13)
--------------------------

- Bug fix: remove user file (`#73 <https://github.com/brazil-data-cube/sample-db/issues/73>`_).

- Bug fix: Add alter sequence owned by table_name (`#70 <https://github.com/brazil-data-cube/sample-db/issues/70>`_).

- Change dataset_table_name to dataset_table_id (`#68 <https://github.com/brazil-data-cube/sample-db/issues/68>`_).


Version 0.6.1 (2021-07-07)
--------------------------

- Remove the sample-db-utils as required (`#65 <https://github.com/brazil-data-cube/sample-db-utils/issues/65>`_).

- Bug Fix:  Add index in collection_date (`#64 <https://github.com/brazil-data-cube/sample-db-utils/issues/64>`_).

- Add delete dataset in cli.py (`#63 <https://github.com/brazil-data-cube/sample-db-utils/issues/#63>`_).


Version 0.6.0 (2021-04-22)
--------------------------

- Drone integration (`#34 <https://github.com/brazil-data-cube/sample-db-utils/issues/34>`_).

- Review model  (`#39 <https://github.com/brazil-data-cube/sample-db-utils/issues/39>`_).

- Organize repository and remove old codes (`#35 <https://github.com/brazil-data-cube/sample-db-utils/issues/35>`_).

- Add Geometry in observation (`#19 <https://github.com/brazil-data-cube/sample-db-utils/issues/19>`_).

- Change Alembic to Flask-Alembic (`#26 <https://github.com/brazil-data-cube/sample-db-utils/issues/26>`_).

- Add minimum test (`#44 <https://github.com/brazil-data-cube/sample-db-utils/issues/44>`_).

- Command Line Interface (CLI).

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Installation and build instructions.

- Usage instructions.

- Package support through Setuptools.

- License: `MIT <https://github.com/gqueiroz/wtss.py/blob/master/LICENSE>`_.
