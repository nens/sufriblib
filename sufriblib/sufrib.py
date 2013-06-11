# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Defines classes RIB21 and RMB21 that can hold the data of SUFRIB 2.1
RIB and RMB files, and helper classes."""


# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from . import errors


class RibLine(object):
    FIELDS = ()
    """Base class for RIB line classes"""
    def parse(self, line_number, line):
        fields = self.FIELDS
        line_fields = line.split('|')

        if len(line_fields) != len(fields):
            return [
                errors.Error(
                    line_number,
                    ("Regel heeft {line_fields} velden, "
                    "verwachtte er {expected_fields}"),
                    {'line_fields': len(line_fields),
                     'expected_fields': len(fields)})
                ]

        for field_num, (fieldname, expected_length) in enumerate(fields):
            if len(line_fields[field_num]) != expected_length:
                return [
                    errors.Error(
                        line_number,
                        ("Het {fieldnr}e veld, {name}, is {l} "
                         "tekens lang, moet {e} zijn"),
                        {'fieldnr': field_num + 1,
                         'name': fieldname,
                         'l': len(line_fields[field_num]),
                         'e': expected_length})]
            setattr(self, fieldname, line_fields[field_num])

        return self.check_contents()

    def check_contents(self):
        return []  # Default = no errors = success


class AlgeLine(RibLine):
    FIELDS = (
        ('record_type', 5),
        ('ABA', 15),
        ('AAM', 30),
        ('AAN', 30),
        ('ABB', 15),
        ('ABE', 1),
        ('ABH', 60),
        ('ABI', 15),
        ('ABJ', 15),
        ('ABP', 1),
        ('ADF', 60),
        ('ABR', 64))


class RiooLine(RibLine):
    FIELDS = (
        ('record_type', 5),
        ('AAA', 30),
        ('AAB', 30),
        ('AAC', 19),
        ('AAD', 30),
        ('AAE', 19),
        ('AAF', 30),
        ('AAG', 19),
        ('AAH', 6),
        ('AAI', 2),
        ('AAJ', 30),
        ('AAK', 1),
        ('AAL', 2),
        ('AAO', 30),
        ('AAP', 30),
        ('AAQ', 1),
        ('AAS', 30),
        ('ABC', 1),
        ('ABF', 10),
        ('ABG', 5),
        ('ABK', 1),
        ('ABL', 1),
        ('ABM', 1),
        ('ABN', 15),
        ('ABO', 15),
        ('ABQ', 7),
        ('ACA', 2),
        ('ACB', 4),
        ('ACC', 4),
        ('ACD', 2),
        ('ACE', 1),
        ('ACF', 2),
        ('ACG', 5),
        ('ACH', 6),
        ('ACI', 6),
        ('ACJ', 1),
        ('ACK', 1),
        ('ACL', 30),
        ('ACM', 1),
        ('ACN', 9),
        ('ACO', 1),
        ('ACP', 2),
        ('ACQ', 2),
        ('ADA', 1),
        ('ADB', 4),
        ('ADC', 1),
        ('ADE', 120),
        ('ACR', 6),
        ('ACS', 6))


class PutLine(RibLine):
    FIELDS = (
        ('record_type', 4),
        ('CAA', 30),
        ('CAB', 19),
        ('CAJ', 30),
        ('CAL', 2),
        ('CAO', 30),
        ('CAP', 30),
        ('CAQ', 30),
        ('CAR', 2),
        ('CAS', 30),
        ('CBC', 1),
        ('CBD', 1),
        ('CBF', 10),
        ('CBG', 5),
        ('CBK', 1),
        ('CBL', 1),
        ('CBM', 1),
        ('CBN', 15),
        ('CBO', 15),
        ('CCA', 1),
        ('CCB', 4),
        ('CCC', 4),
        ('CCD', 2),
        ('CCG', 4),
        ('CCK', 1),
        ('CCL', 30),
        ('CCM', 1),
        ('CCN', 9),
        ('CCO', 1),
        ('CCP', 2),
        ('CCQ', 4),
        ('CCR', 4),
        ('CCS', 1),
        ('CCT', 1),
        ('CDA', 1),
        ('CDB', 4),
        ('CDC', 1),
        ('CDD', 1),
        ('CDE', 120),
        ('CCU', 6))


class WaarLine(RibLine):
    FIELDS = (
        ('record_type', 5),
        ('ZZA', 6),
        ('ZZB', 1),
        ('ZZC', 1),
        ('ZZD', 2),
        ('ZZE', 30),
        ('ZZF', 3),
        ('ZZG', 5),
        ('ZZH', 2),
        ('ZZI', 15),
        ('ZZJ', 15),
        ('ZZK', 2),
        ('ZZL', 2),
        ('ZZM', 1),
        ('ZZN', 11),
        ('ZZO', 20),
        ('ZZP', 120),
        ('ZZQ', 15),
        ('ZZR', 1),
        ('ZZS', 30),
        ('ZZT', 30),
        ('ZZU', 30),
        ('ZZV', 30))


class MputLine(RibLine):
    FIELDS = (
        ('record_type', 5),
        ('ZYA', 8),
        ('ZYB', 1),
        ('ZYE', 30),
        ('ZYK', 2),
        ('ZYL', 2),
        ('ZYM', 6),
        ('ZYN', 6),
        ('ZYO', 5),
        ('ZYP', 10),
        ('ZYQ', 11),
        ('ZYR', 1),
        ('ZYS', 1),
        ('ZYT', 10),
        ('ZYU', 3),
        ('ZYV', 30),
        ('ZYW', 30),
        ('ZYX', 30),
        ('ZYY', 30),
        ('ZYZ', 30))


class MrioLine(RibLine):
    FIELDS = (
        ('record_type', 5),
        ('ZYA', 8),
        ('ZYB', 1),
        ('ZYE', 30),
        ('ZYK', 2),
        ('ZYL', 2),
        ('ZYM', 6),
        ('ZYN', 6),
        ('ZYO', 5),
        ('ZYP', 10),
        ('ZYQ', 11),
        ('ZYR', 1),
        ('ZYS', 1),
        ('ZYT', 10),
        ('ZYU', 3),
        ('ZYV', 30),
        ('ZYW', 30),
        ('ZYX', 30),
        ('ZYY', 30),
        ('ZYZ', 30))


class SUFRIB21(object):
    LINE_CLASSES = {
        '*ALGE': AlgeLine,
        '*PUT': PutLine,
        '*RIOO': RiooLine,
        '*WAAR': WaarLine,
        '*MPUT': MputLine,
        '*MRIO': MrioLine
        }

    def __init__(self):
        self.lines = []

    def add_line(self, line_number, line, errorlist):
        line = line.strip("\r\n")
        record_type = line.split('|')[0].strip()

        if record_type not in SUFRIB21.LINE_CLASSES:
            errorlist.append(errors.Error(
                    line_number,
                    "Onbekend record type: '{record_type}'",
                    {'record_type': record_type}))
        else:
            line_class = SUFRIB21.LINE_CLASSES[record_type]
            line_instance = line_class()
            line_errors = line_instance.parse(line_number, line)
            if line_errors:
                errorlist += line_errors
            else:
                self.lines.append(line_instance)


class RIB21(SUFRIB21):
    LINE_CLASSES = {
        '*ALGE': AlgeLine,
        '*PUT': PutLine,
        '*RIOO': RiooLine,
        '*WAAR': WaarLine,
        }


class RMB21(SUFRIB21):
    LINE_CLASSES = {
        '*ALGE': AlgeLine,
        '*MPUT': MputLine,
        '*MRIO': MrioLine
        }
