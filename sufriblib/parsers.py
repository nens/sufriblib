# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Parsing RIB and RMB files."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

from .errors import Error

from . import sufrib


def parse(path):
    errors = []

    ribfile = parse_collecting_errors(errors, path)

    if errors:
        return None, errors
    else:
        return ribfile, []


def parse_collecting_errors(errors, path):
    if not os.path.exists(path):
        errors.append(
            Error(None, "'{path}' bestaat niet.", {'path': path}))
        return

    if path.lower().endswith(".rmb"):
        sufribobject = sufrib.RMB21()
    else:
        sufribobject = sufrib.RIB21()

    try:
        sufribfile = file(path, 'rU')
    except IOError as e:
        errors.append(
            Error(
                None,
                "Openen van bestand '{path}' resulteerde in {exception}.",
                {'path': path, 'exception': unicode(e)}))

    for line_number, line in enumerate(sufribfile, 1):
        sufribobject.add_line(line_number, line, errors)

    return sufribobject
