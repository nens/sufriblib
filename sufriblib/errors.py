# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Module defining error objects."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class Error(object):
    def __init__(self, line_number, message, arguments):
        self.line_number = line_number
        self.message = message
        self.arguments = arguments

    def format(self, use_line_number=False):
        if self.line_number and use_line_number:
            return (("Fout op regel {0}: ").format(self.line_number) +
                    self.message.format(**self.arguments))
        else:
            return (self.message.format(**self.arguments))

    def __unicode__(self):
        return self.format()
