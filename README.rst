sufriblib
=========

Parse .RIB and .RMB files according to the SUFRIB 2.1 standard.

For their specification, see the included PDF "UNIFORMERING RIOOL
INSPECTIEBESTANDEN SUFRIB versie 2.1 revisie 0 28-08-2007-1.pdf".

Usage
=====

The main two functions are in sufriblib.parsers;

    rib, errors = sufriblib.parsers.parse_rib(path)

    rmb, errors = sufriblib.parsers.parse_rmb(path)

If there are errors, errors is a list containing them and rib/rmb will
be None; if there are no errors, rib will be a sufriblib.rib.RIB
object and rmb will be a sufriblib.rmb.RMB object and errors will be
an empty list.
