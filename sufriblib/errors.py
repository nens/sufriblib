# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Module defining error objects."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import collections

Error = collections.namedtuple("Error", "line_number message")
