# -*- coding: utf-8 -*-
from __future__ import division

import unittest

from .query_ircelsos import query_ircelsos

class TestQuery(unittest.TestCase):

    def test_date_parsing(self):

        with self.assertRaises(ValueError):
            query_ircelsos('bc', utc_start='2012-01-01T09:00:00:00')

        with self.assertRaises(ValueError):
            query_ircelsos('bc', utc_end='2012-01-01T09:00:00:00')
