# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 21:50:53 2015

@author: Joris Van den Bossche
"""

import datetime

from owslib.sos import SensorObservationService

sos = SensorObservationService("http://sos.irceline.be/sos")

pollutants = sos.contents.keys()

SAROAD_CODE = {'o3': '44201 - O3',
               'no2': '42602 - NO2',
               'pm10': '81102 - PM10',
               'pm25': '81104 - PM2.5',
               'so2': '42401 - SO2',
               'co': '42101 - CO',
               'bc': '16111 - Black Carbon'}


def query_ircelsos(pol, station=None, utc_start=None, utc_end=None):
    """
    Parameters
    ----------
    pol : str or list of str
    station :
    utc_start, utc_end : datetime.datetime or string

    """

    # check pollutant
    if pol not in pollutants:
        try:
            pol = SAROAD_CODE[pol]
        except KeyError:
            raise KeyError("Pollutant '{0}' not recognized".format(pol))

    if not isinstance(pol, list):
        pol = [pol]

    # check start and end
    if isinstance(utc_start, datetime.datetime):
        utc_start = datetime.datetime.strftime(utc_start, '%Y-%m-%dT%H:%M:%S')
    if isinstance(utc_end, datetime.datetime):
        utc_end = datetime.datetime.strftime(utc_end, '%Y-%m-%dT%H:%M:%S')

    offerings = pol
    observedProperties = pol
    responseFormat = 'text/xml;subtype="om/1.0.0"'
    kwds = {}
    if station:
        kwds['featureofinterest'] = station
    kwds['eventTime'] = utc_start + '/' + utc_end

    response = sos.get_observation(offerings=offerings, responseFormat=responseFormat,
                                   observedProperties=observedProperties, **kwds)

    return response


#response = query_ircelsos('o3', 'BETN060', '2015-03-27T00:00:00', '2015-03-27T10:00:00')
