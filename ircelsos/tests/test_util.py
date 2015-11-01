# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest

import pytest

from ircelsos.util import print_stations, print_pollutants
from ircelsos import metadata


def strip(s):
    s = s.splitlines()
    s = [line.strip() for line in s]
    s = "\n".join(s)
    return s


@pytest.mark.usefixtures("capsys")
class TestTablePrinting():

    def test_print_stations(self, capsys):

        stations = {st: metadata.STATIONS[st] for st in ('BETR801', 'BETR802')}
        print_stations(stations)
        out, err = capsys.readouterr()
        expected = """name   | id      | description
-------+---------+----------------
42R801 | BETR801 | urban - Traffic
42R802 | BETR802 | urban - Traffic
"""
        assert strip(out) == strip(expected)

    def test_print_pollutants(self, capsys):

        pols = {pol: metadata.POLLUTANTS[pol] for pol in
                    ('42602 - NO2', '44201 - O3')}
        print_pollutants(pols)
        out, err = capsys.readouterr()
        expected = """id          | name
------------+-----------------
42602 - NO2 | Nitrogen dioxide
44201 - O3  | Ozone
"""
        assert strip(out) == strip(expected)
