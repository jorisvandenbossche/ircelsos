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

        print_stations(['BETR801', 'BETR802'])
        out, err = capsys.readouterr()
        expected = """name   | EU_code | location   | region | type
-------+---------+------------+--------+--------
42R801 | BETR801 | Borgerhout | urban  | Traffic
42R802 | BETR802 | Borgerhout | urban  | Traffic
"""
        assert strip(out) == strip(expected)

    def test_print_pollutants(self, capsys):

        print_pollutants(['42602 - NO2', '44201 - O3'])
        out, err = capsys.readouterr()
        expected = """id          | short | name             | stations
------------+-------+------------------+---------
42602 - NO2 | no2   | Nitrogen dioxide | 105
44201 - O3  | o3    | Ozone            | 47
"""
        assert strip(out) == strip(expected)
