# -*- coding: utf-8 -*-
from __future__ import print_function, division

import unittest
import os

from ircelsos.sos import get_sos, ircelsos_data_dir


class TestSosConnection(unittest.TestCase):

    def setUp(self):
        # ensure a capabilities_test.xml is in the data_dir
        # I read/write it to ensure it is a recent file and this
        # test should work offline

        filename = os.path.realpath(__file__)
        base_dir = os.path.abspath(os.path.dirname(filename))

        data_dir = ircelsos_data_dir()
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        xml_file = os.path.join(data_dir, 'capabilities_test.xml')

        with open(os.path.join(base_dir, 'data', 'capabilities.xml')) as f:
            with open(xml_file, 'w') as f_out:
                f_out.write(f.read())

        self.xml_file = xml_file

    def tearDown(self):
        try:
            os.remove(self.xml_file)
        except:
            pass

    def test_capabilities_from_file(self):
        # testing in case the file does not exist will be done on travis
        # in any case, this tests if the file is there
        SOS = get_sos(self.xml_file)
