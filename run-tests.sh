#!/usr/bin/env bash
#
# This file is part of Sample Database Model.
# Copyright (C) 2019-2020 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

pydocstyle --match-dir="^sample_db/alembic" sample_db setup.py && \
isort sample_db setup.py --check-only --diff --skip-glob "sample_db/alembic/*" && \
check-manifest --ignore ".travis-*" --ignore ".readthedocs.*" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
pytest