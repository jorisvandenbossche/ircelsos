# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest

from ircelsos.parser import get_observations, parse_observation


class TestParser(unittest.TestCase):

    def setUp(self):

        import os

        filename = os.path.realpath(__file__)
        base_dir = os.path.abspath(os.path.dirname(filename))

        with open(os.path.join(base_dir, 'data', 'observation.xml')) as f:
            self.obs_xml = f.read()

    def test_get_observations(self):

        obs = get_observations(self.obs_xml)
        self.assertEqual(len(obs), 37)

        obs1 = obs[0]
        self.assertTrue('Observation' in obs1.tag)

    def test_parse_observation(self):

        obs = get_observations(self.obs_xml)
        obs1 = obs[0]

        st_info, raw_data = parse_observation(obs1)

        expected = {'description': 'suburban - Industrial',
                    'id': 'BETM705',
                    'long_name': '44M705 - ROESELARE',
                    'name': '44M705'}
        self.assertDictEqual(st_info, expected)

        raw_data_expected = '2015-03-27T01:00:00.000+01:00,67.5;2015-03-27T02:00:00.000+01:00,65.5;2015-03-27T03:00:00.000+01:00,64.5;2015-03-27T04:00:00.000+01:00,65.0;2015-03-27T05:00:00.000+01:00,62.5;2015-03-27T06:00:00.000+01:00,57.0;2015-03-27T07:00:00.000+01:00,32.5;2015-03-27T08:00:00.000+01:00,25.0;2015-03-27T09:00:00.000+01:00,37.5;2015-03-27T10:00:00.000+01:00,59.0;2015-03-27T11:00:00.000+01:00,65.5;'
        self.assertEqual(raw_data, raw_data_expected)
