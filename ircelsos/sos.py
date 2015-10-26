# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:16:17 2015

@author: Joris Van den Bossche
"""
from __future__ import print_function

import sys
import os
import datetime
from xml.etree import ElementTree

import requests
from owslib.sos import SensorObservationService


BASE_URL = 'http://sos.irceline.be/sos'


def get_sos():
    """Return a SensorObservationService instance"""

    data_dir = ircelsos_data_dir()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    xml_file = os.path.join(data_dir, 'capabilities.xml')

    if os.path.isfile(xml_file):
        xml = file(xml_file).read()
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
            with open(xml_file, 'w') as xml:
                xml.write(ElementTree.tostring(sos._capabilities))
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
