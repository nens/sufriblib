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


def enumerate_file(path):
    """Opens file, deals with strange characters, and yields pairs
    of (line_number, stripped line). Line numbers start with 1. May
    raise IOError."""
    sufribfile = file(path, 'rU')  # All-platform line endings

    for line_number, line in enumerate(sufribfile, 1):
        # By decoding from and encoding to ASCII, all non-ASCII
        # characters end up as '?'. The SUFRIB standard prescribes
        # ASCII, but this seems less harsh than throwing an error.
        line = line.decode('ascii', 'replace')
        line = line.encode('ascii', 'replace')

        line = line.strip("\r\n")  # Don't strip spaces! The last
                                   # field on a line must have the
                                   # right size, and that often means
                                   # trailing spaces are necessary.

        yield (line_number, line)


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
        for line_number, line in enumerate_file(path):
            sufribobject.add_line(line_number, line, errors)
    except IOError as e:
        errors.append(
            Error(
                None,
                "Openen van bestand '{path}' resulteerde in {exception}.",
                {'path': path, 'exception': unicode(e)}))

    return sufribobject
