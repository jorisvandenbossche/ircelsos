# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest
import datetime

import pytest

import ircelsos
from ircelsos.query_ircelsos import query_ircelsos
from ircelsos.parser import get_observations, parse_observation

try:
    import pandas as pd
    from pandas.util.testing import assert_frame_equal
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


@pytest.mark.skipif(not HAS_PANDAS, reason='Skipping interactive tests because '
                                           'pandas is not installed.')
class TestInteractiveQuery(unittest.TestCase):

    @pytest.mark.network
    def test_query(self):

        df = ircelsos.query(pollutant='o3', station='BETN060',
                            utc_start='2015-03-27T00:00:00',
                            utc_end='2015-03-27T3:00:00')

        expected = pd.DataFrame({'43N060':
                                 {'2015-03-27T01:00:00.000+01:00': 48.0,
                                  '2015-03-27T02:00:00.000+01:00': 51.0,
                                  '2015-03-27T03:00:00.000+01:00': 52.0,
                                  '2015-03-27T04:00:00.000+01:00': 47.5}})
        expected.index.name = 'time'

        assert_frame_equal(df, expected)
