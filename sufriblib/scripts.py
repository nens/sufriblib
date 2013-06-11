# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

""" """

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import argparse
import os
import sys

from . import parsers


def sufribcat():
    parser = argparse.ArgumentParser(
 description="Read a .RIB or .RMB SUFRIB 2.1 file, and print errors "
             "or a copy of the file.")
    parser.add_argument("filename")

    path = parser.parse_args().filename

    if not os.path.exists(path) or not os.path.isfile(path):
        print("Not a readable file: {path}".format(path=path))
        sys.exit(1)

    if not (path.lower().endswith(".rib") or path.lower().endswith("rmb")):
        print("Not a .RIB or .RMB file: {path}".format(path=path))
        sys.exit(1)

    ob, errors = parsers.parse(path)
    if errors:
        for error in errors:
            print(unicode(error))
    else:
            print(unicode(ob))
