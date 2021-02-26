#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Allows the client command interface to be run from the package."""
from .cli import main

if __name__ == '__main__':
    main(as_module=True)
