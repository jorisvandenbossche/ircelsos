# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest

from ircelsos.query_ircelsos import query_ircelsos
from ircelsos.parser import get_observations, parse_observation

class TestQuery(unittest.TestCase):

    def test_query_and_parse(self):

        # small test example
        pollutant = 'o3'
        station = 'BETN060'
        period1 = '2015-03-27T00:00:00'
        period2 = '2015-03-27T10:00:00'
        response = query_ircelsos(pollutant, station, period1, period2)
        observations = get_observations(response)
        st_info, raw_data = parse_observation(observations[0])

        st_info_expected = {'description': 'unknown - Unknown',
                            'id': 'BETN060',
                            'long_name': '43N060 - HAVINNES',
                            'name': '43N060'}
        self.assertDictEqual(st_info, st_info_expected)

        raw_data_expected = '2015-03-27T01:00:00.000+01:00,48.0;2015-03-27T02:00:00.000+01:00,51.0;2015-03-27T03:00:00.000+01:00,52.0;2015-03-27T04:00:00.000+01:00,47.5;2015-03-27T05:00:00.000+01:00,45.0;2015-03-27T06:00:00.000+01:00,40.5;2015-03-27T07:00:00.000+01:00,25.0;2015-03-27T08:00:00.000+01:00,17.0;2015-03-27T09:00:00.000+01:00,23.0;2015-03-27T10:00:00.000+01:00,42.5;2015-03-27T11:00:00.000+01:00,49.0;'
        self.assertEqual(raw_data, raw_data_expected)

    def test_date_parsing(self):

        import dateutil
        print(dateutil.__version__)
        with self.assertRaises(ValueError):
            query_ircelsos('bc', utc_start='2012-01-01T09:00:00:00')

        with self.assertRaises(ValueError):
            query_ircelsos('bc', utc_end='2012-01-01T09:00:00:00')
