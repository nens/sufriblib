# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Defines classes RIB21 and RMB21 that can hold the data of SUFRIB 2.1
RIB and RMB files, and helper classes."""


# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from . import util
from .errors import Error


class RibLine(object):
    FIELDS = ()
    """Base class for RIB line classes"""
    def parse(self, line_number, line):
        self.line_number = line_number

        fields = self.FIELDS
        line_fields = line.split('|')

        if len(line_fields) != len(fields):
            return [
                Error(line_number=line_number,
                      message=("Regel heeft {line_fields} velden, "
                               "verwachtte er {expected_fields}")
                      .format(line_fields=len(line_fields),
                              expected_fields=len(fields)))
                ]

        for (field_num, (fieldname, expected_length, format)
             ) in enumerate(fields):
            field = line_fields[field_num]
            # Check for length
            if len(field) != expected_length:
                return [
                    Error(
                        line_number=line_number,
                        message=("Het {fieldnr}e veld, {name}, is {l} "
                                 "tekens lang, moet {e} zijn")
                        .format(fieldnr=field_num + 1,
                                name=fieldname,
                                l=len(field),
                                e=expected_length))]

            # Note that we don't check for required fields here, so if
            # a field consists of just spaces, we record its value as None.
            if field is None or field.isspace():
                setattr(self, fieldname, None)
            # But if there is something in the field, if there is a
            # format for this field (or some other processing on the
            # field, like stripping) check for it
            elif format is not None:
                interpreted_field, correct = check_format(format, field)
                if correct:
                    setattr(self, fieldname, interpreted_field)
                else:
                    return [
                        Error(
                            line_number=line_number,
                            message=(
                                "Het {fieldnr}e veld, {name}, heeft als "
                                "inhoud '{content}' en dat is niet van de vorm "
                                "'{format}'")
                            .format(
                                fieldnr=field_num + 1,
                                name=fieldname,
                                content=field,
                                format=format))]
            else:
                # Otherwise just use the field verbatim
                setattr(self, fieldname, field)

        return self.check()  # For line-specific checks

    def check(self):
        return []  # Default, no errors, override in subclasses


class AlgeLine(RibLine):
    FIELDS = (
        ('record_type', 5, None),
        ('ABA', 15, None),
        ('AAM', 30, None),
        ('AAN', 30, None),
        ('ABB', 15, None),
        ('ABE', 1, None),
        ('ABH', 60, None),
        ('ABI', 15, None),
        ('ABJ', 15, None),
        ('ABP', 1, None),
        ('ADF', 60, None),
        ('ABR', 64, None))


class RiooLine(RibLine):
    FIELDS = (
        ('record_type', 5, None),
        ('AAA', 30, None),
        ('AAB', 30, None),
        ('AAC', 19, None),
        ('AAD', 30, None),
        ('AAE', 19, '######.##/######.##'),
        ('AAF', 30, None),
        ('AAG', 19, '######.##/######.##'),
        ('AAH', 6, None),
        ('AAI', 2, None),
        ('AAJ', 30, None),
        ('AAK', 1, None),
        ('AAL', 2, None),
        ('AAO', 30, None),
        ('AAP', 30, None),
        ('AAQ', 1, None),
        ('AAS', 30, None),
        ('ABC', 1, None),
        ('ABF', 10, None),
        ('ABG', 5, None),
        ('ABK', 1, None),
        ('ABL', 1, None),
        ('ABM', 1, None),
        ('ABN', 15, None),
        ('ABO', 15, None),
        ('ABQ', 7, None),
        ('ACA', 2, None),
        ('ACB', 4, 'float'),
        ('ACC', 4, None),
        ('ACD', 2, None),
        ('ACE', 1, None),
        ('ACF', 2, None),
        ('ACG', 5, None),
        ('ACH', 6, None),
        ('ACI', 6, None),
        ('ACJ', 1, None),
        ('ACK', 1, None),
        ('ACL', 30, None),
        ('ACM', 1, None),
        ('ACN', 9, None),
        ('ACO', 1, None),
        ('ACP', 2, None),
        ('ACQ', 2, None),
        ('ADA', 1, None),
        ('ADB', 4, None),
        ('ADC', 1, None),
        ('ADE', 120, None),
        ('ACR', 6, 'float'),
        ('ACS', 6, 'float'))

    def check(self):
        errors = []

        if self.AAA is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message=(
                "Verplicht veld AAA (strengreferentie) is niet ingevuld")))

        if self.AAD is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message=("Verplicht veld AAD (knooppuntreferentie 1) "
                             "is niet ingevuld")))

        if self.AAF is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message=("Verplicht veld AAF (knooppuntreferentie 2) "
                             "is niet ingevuld")))
        return errors

    @property
    def sewer_id(self):
        return self.AAA.strip() if self.AAA is not None else None

    @property
    def manhole1_id(self):
        return self.AAD.strip() if self.AAD is not None else None

    @property
    def manhole2_id(self):
        return self.AAF.strip() if self.AAF is not None else None

    @property
    def manhole1_wgs84_point(self):
        """Already checked, only need to translate to WGS84."""
        if self.AAE is None:
            return None

        return util.rd_to_wgs84(*self.AAE)

    @property
    def manhole1_rd_point(self):
        """Useful for distance computations"""
        return self.AAE

    @property
    def manhole2_wgs84_point(self):
        """Already checked, only need to translate to WGS84."""
        if self.AAG is None:
            return None

        return util.rd_to_wgs84(*self.AAG)

    @property
    def manhole2_rd_point(self):
        """Useful for distance computations"""
        return self.AAG


class PutLine(RibLine):
    FIELDS = (
        ('record_type', 4, None),
        ('CAA', 30, None),
        ('CAB', 19, '######.##/######.##'),
        ('CAJ', 30, None),
        ('CAL', 2, None),
        ('CAO', 30, None),
        ('CAP', 30, None),
        ('CAQ', 30, None),
        ('CAR', 2, None),
        ('CAS', 30, None),
        ('CBC', 1, None),
        ('CBD', 1, None),
        ('CBF', 10, None),
        ('CBG', 5, None),
        ('CBK', 1, None),
        ('CBL', 1, None),
        ('CBM', 1, None),
        ('CBN', 15, None),
        ('CBO', 15, None),
        ('CCA', 1, None),
        ('CCB', 4, None),
        ('CCC', 4, None),
        ('CCD', 2, None),
        ('CCG', 4, None),
        ('CCK', 1, None),
        ('CCL', 30, None),
        ('CCM', 1, None),
        ('CCN', 9, None),
        ('CCO', 1, None),
        ('CCP', 2, None),
        ('CCQ', 4, None),
        ('CCR', 4, None),
        ('CCS', 1, None),
        ('CCT', 1, None),
        ('CDA', 1, None),
        ('CDB', 4, None),
        ('CDC', 1, None),
        ('CDD', 1, None),
        ('CDE', 120, None),
        ('CCU', 6, None))

    @property
    def putid(self):
        """Putid is CAA stripped, or None if nothing there"""
        return self.CAA.strip() or None

    @property
    def wgs84_point(self):
        """Already checked, only need to translate to WGS84."""
        if self.CAB is None:
            return None

        return util.rd_to_wgs84(*self.CAB)

    @property
    def rd_point(self):
        """Useful for length calculations"""
        return self.CAB

    @property
    def is_sink(self):
        return self.CAR == 'Xs'  # Entirely Almere-specific

    def check(self):
        errors = []
        if self.putid is None:
            errors.append(
                Error(
                    line_number=self.line_number,
                    message="Geen knooppunt referentie"))
        if self.CAB is None:
            errors.append(
                Error(
                    line_number=self.line_number,
                    message="Geen knooppunt coordinaat"))
        return errors


class WaarLine(RibLine):
    FIELDS = (
        ('record_type', 5, None),
        ('ZZA', 6, None),
        ('ZZB', 1, None),
        ('ZZC', 1, None),
        ('ZZD', 2, None),
        ('ZZE', 30, None),
        ('ZZF', 3, None),
        ('ZZG', 5, None),
        ('ZZH', 2, None),
        ('ZZI', 15, None),
        ('ZZJ', 15, None),
        ('ZZK', 2, None),
        ('ZZL', 2, None),
        ('ZZM', 1, None),
        ('ZZN', 11, None),
        ('ZZO', 20, None),
        ('ZZP', 120, None),
        ('ZZQ', 15, None),
        ('ZZR', 1, None),
        ('ZZS', 30, None),
        ('ZZT', 30, None),
        ('ZZU', 30, None),
        ('ZZV', 30, None))


class MputLine(RibLine):
    FIELDS = (
        ('record_type', 5, None),
        ('ZYA', 8, None),
        ('ZYB', 1, None),
        ('ZYE', 30, None),
        ('ZYK', 2, None),
        ('ZYL', 2, None),
        ('ZYM', 6, None),
        ('ZYN', 6, None),
        ('ZYO', 5, None),
        ('ZYP', 10, None),
        ('ZYQ', 11, None),
        ('ZYR', 1, None),
        ('ZYS', 1, None),
        ('ZYT', 10, None),
        ('ZYU', 3, None),
        ('ZYV', 30, None),
        ('ZYW', 30, None),
        ('ZYX', 30, None),
        ('ZYY', 30, None),
        ('ZYZ', 30, None))


class MrioLine(RibLine):
    FIELDS = (
        ('record_type', 5, None),
        ('ZYA', 8, 'float'),
        ('ZYB', 1, None),
        ('ZYE', 30, None),
        ('ZYK', 2, None),
        ('ZYL', 2, None),
        ('ZYM', 6, None),
        ('ZYN', 6, None),
        ('ZYO', 5, None),
        ('ZYP', 10, None),
        ('ZYQ', 11, None),
        ('ZYR', 1, None),
        ('ZYS', 1, None),
        ('ZYT', 10, 'float'),
        ('ZYU', 3, 'int'),
        ('ZYV', 30, None),
        ('ZYW', 30, None),
        ('ZYX', 30, None),
        ('ZYY', 30, None),
        ('ZYZ', 30, None))

    @property
    def sewer_id(self):
        if not self.ZYE or self.ZYE.isspace():
            return None
        return self.ZYE.strip()

    @property
    def distance(self):
        return self.ZYA

    @property
    def measurement(self):
        if self.ZYU is None:
            return self.ZYT
        else:
            return self.ZYT * (10 ** self.ZYU)

    def check(self):
        errors = []

        if self.sewer_id is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message="Veld ZYE (Streng identificatie) ontbreekt"))

        if self.distance is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message="Veld ZYA (Afstand) ontbreekt"))

        if self.ZYB is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message="Veld ZYB (Richting referentie) ontbreekt"))
        elif self.ZYB not in "12":
            errors.append(Error(
                    line_number=self.line_number,
                    message="Veld ZYB (Richting referentie) moet 1 of 2 zijn"))

        if self.ZYT is None:
            errors.append(Error(
                    line_number=self.line_number,
                    message="Veld ZYT (Meetwaarde) ontbreekt"))

        return errors


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
            errorlist.append(Error(
                    line_number=line_number,
                    message="Onbekend record type: '{record_type}'"
                    .format(record_type=record_type)))
        else:
            line_class = SUFRIB21.LINE_CLASSES[record_type]
            line_instance = line_class()
            line_errors = line_instance.parse(line_number, line)
            if line_errors:
                errorlist += line_errors
            else:
                self.lines.append(line_instance)

    def lines_of_type(self, record_type):
        return [line for line in self.lines
                if line.record_type == record_type]


class RIB21(SUFRIB21):
    LINE_CLASSES = {
        '*ALGE': AlgeLine,
        '*PUT': PutLine,
        '*RIOO': RiooLine,
        '*WAAR': WaarLine,
        }

    def __unicode__(self):
        s = "RIB21 bestand. Regels:\n"
        for line in self.lines:
            s += unicode(line) + "\n"

        return s


class RMB21(SUFRIB21):
    LINE_CLASSES = {
        '*ALGE': AlgeLine,
        '*MPUT': MputLine,
        '*MRIO': MrioLine
        }


def check_format(format, field):
    success = False
    result = None

    if format == 'float':
        try:
            result = float(field)
            success = True
        except ValueError:
            success = False
            result = None

    elif format == 'int':
        try:
            result = int(field)
            success = True
        except ValueError:
            success = False
            result = None

    elif format == 'stripped_string':
        success = True  # Always correct
        result = field.strip()

    elif format == "######.##/######.##":
        parts = field.split("/")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            result = False
        else:
            try:
                result = (float(parts[0]), float(parts[1]))
                success = True
            except ValueError:
                success = False

    return result, success
