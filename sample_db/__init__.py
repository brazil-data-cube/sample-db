#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Python Sample Database Model."""

from .ext import BDCSample
from .version import __version__

__all__ = ('__version__',
           'BDCSample',)
