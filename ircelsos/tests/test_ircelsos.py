# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest
import datetime

import pytest

from ircelsos.query_ircelsos import query_ircelsos
from ircelsos.parser import get_observations, parse_observation


class TestQuery(unittest.TestCase):

    @pytest.mark.network
    def test_query_and_parse(self):

        # small test example
        pollutant = 'o3'
        station = 'BETN060'
        period1 = '2015-03-27T00:00:00'
        period2 = '2015-03-27T10:00:00'
        response = query_ircelsos(pollutant, station, period1, period2)
        observations = get_observations(response)
        obs_info, raw_data = parse_observation(observations[0])

        obs_info_expected = {'sampling_time':
                             ['2015-03-27T01:00:00.000+01:00',
                              '2015-03-27T11:00:00.000+01:00'],
                             'feature_of_interest':
                             {'description': 'unknown - Unknown',
                              'id': 'BETN060',
                              'long_name': '43N060 - Havinnes',
                              'name': '43N060'}}
        self.assertDictEqual(obs_info, obs_info_expected)

        raw_data_expected = '2015-03-27T01:00:00.000+01:00,48.0;2015-03-27T02:00:00.000+01:00,51.0;2015-03-27T03:00:00.000+01:00,52.0;2015-03-27T04:00:00.000+01:00,47.5;2015-03-27T05:00:00.000+01:00,45.0;2015-03-27T06:00:00.000+01:00,40.5;2015-03-27T07:00:00.000+01:00,25.0;2015-03-27T08:00:00.000+01:00,17.0;2015-03-27T09:00:00.000+01:00,23.0;2015-03-27T10:00:00.000+01:00,42.5;2015-03-27T11:00:00.000+01:00,49.0;'
        self.assertEqual(raw_data, raw_data_expected)

    def test_date_parsing(self):

        from ircelsos.query_ircelsos import _check_start_end

        # basic case with strings
        result = _check_start_end('2012-01-01T01:00:00', '2012-01-01T09:00:00')
        expected = '2012-01-01T01:00:00/2012-01-01T09:00:00'
        self.assertEqual(result, expected)

        # basic case with datetimes
        result = _check_start_end(datetime.datetime(2012, 1, 1, 1),
                                  datetime.datetime(2012, 1, 1, 9))
        expected = '2012-01-01T01:00:00/2012-01-01T09:00:00'
        self.assertEqual(result, expected)

        # invalid date strings raise error
        with self.assertRaises(ValueError):
            _check_start_end(utc_start='2012-01-01T09:00:00:00', utc_end=None)

        with self.assertRaises(ValueError):
            _check_start_end(utc_start='2012-01-01T01:00:00',
                             utc_end='2012-01-01T09:00:00:00')

        # not specifying anythin

    def test_station_parsing(self):

        from ircelsos.query_ircelsos import _process_sos_kwargs

        # string
        _, station, _ = _process_sos_kwargs('bc', station='BETR801')
        expected = 'BETR801'
        self.assertEqual(station, expected)

        # list of strings
        _, station, _ = _process_sos_kwargs('bc',
                                            station=['BETR801', 'BETR802'])
        expected = 'BETR801,BETR802'
        self.assertEqual(station, expected)

        # local code
        _, station, _ = _process_sos_kwargs('bc', station='42R801')
        expected = 'BETR801'
        self.assertEqual(station, expected)

        # list of local codes
        _, station, _ = _process_sos_kwargs('bc',
                                            station=['42R801', '42R802'])
        expected = 'BETR801,BETR802'
        self.assertEqual(station, expected)

    def test_pollutant_parsing(self):

        from ircelsos.query_ircelsos import _process_sos_kwargs

        # use of short form
        pollutant, _, _ = _process_sos_kwargs('bc')
        expected = ['16111 - Black Carbon']
        self.assertEqual(pollutant, expected)

        # long form passed through
        pollutant, _, _ = _process_sos_kwargs(pollutant='16111 - Black Carbon')
        expected = ['16111 - Black Carbon']
        self.assertEqual(pollutant, expected)

        # raise on invalid
        with self.assertRaises(ValueError):
            pollutant, _, _ = _process_sos_kwargs('invalid')

        # list of strings
        pollutant, _, _ = _process_sos_kwargs(pollutant=['bc', 'no2'])
        expected = ['16111 - Black Carbon', '42602 - NO2']
        self.assertEqual(pollutant, expected)
