# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:16:17 2015

@author: Joris Van den Bossche
"""
from __future__ import print_function

import sys
import os
from io import open
import datetime
from xml.etree.ElementTree import ElementTree

import requests
from owslib.sos import SensorObservationService


BASE_URL = 'http://sos.irceline.be/sos'


def get_sos(xml_file=None):
    """Return a SensorObservationService instance"""

    if xml_file is None:
        data_dir = ircelsos_data_dir()
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        xml_file = os.path.join(data_dir, 'capabilities.xml')

    if os.path.isfile(xml_file):
        xml = open(xml_file, 'rb').read()
        adapted = datetime.datetime.fromtimestamp(os.path.getmtime(xml_file))
        outdated = (datetime.datetime.now() - adapted) > datetime.timedelta(1)
    else:
        xml = None
        outdated = True

    if not outdated:
        sos = SensorObservationService(BASE_URL, xml=xml)
    else:
        try:
            sos = SensorObservationService(BASE_URL)
        except requests.ConnectionError:
            sos = SensorObservationService(BASE_URL, xml=xml)
        else:
            with open(xml_file, 'wb') as xml:
                ElementTree(sos._capabilities).write(xml)
    return sos


def ircelsos_data_dir():
    """Get the data directory

    Adapted from jupyter_core
    """
    home = os.path.expanduser('~')

    if sys.platform == 'darwin':
        return os.path.join(home, 'Library', 'ircelsos')
    elif os.name == 'nt':
        appdata = os.environ.get('APPDATA', os.path.join(home, '.local', 'share'))
        return os.path.join(appdata, 'ircelsos')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = os.environ.get("XDG_DATA_HOME", os.path.join(home, '.local', 'share'))
        return os.path.join(xdg, 'ircelsos')
