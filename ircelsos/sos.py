# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:16:17 2015

@author: Joris Van den Bossche
"""
from __future__ import print_function

from owslib.sos import SensorObservationService


def get_sos():
    """Return a SensorObservationService instance"""

    return SensorObservationService("http://sos.irceline.be/sos")
