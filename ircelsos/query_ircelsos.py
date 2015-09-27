# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 21:50:53 2015

@author: Joris Van den Bossche
"""

import datetime
import dateutil

import six

from . import SOS

POLLUTANTS = list(SOS.contents.keys())

SAROAD_CODE = {'o3': '44201 - O3',
               'no2': '42602 - NO2',
               'pm10': '81102 - PM10',
               'pm25': '81104 - PM2.5',
               'so2': '42401 - SO2',
               'co': '42101 - CO',
               'bc': '16111 - Black Carbon'}


def _check_date(date):
    """Ensure correctly formatted string"""

    if isinstance(date, six.string_types):
        try:
            date = dateutil.parser.parse(date)
        except ValueError:
            msg = "Start date '{0}' not recognized as a valid date".format(date)
            raise ValueError(msg)

    if isinstance(date, datetime.date):
        date = datetime.datetime.strftime(date, '%Y-%m-%dT%H:%M:%S')

    return date


def _check_start_end(utc_start, utc_end):
    """Check start/end and convert to combined value"""

    if utc_end is not None and utc_start is None:
        raise ValueError("'utc_start' cannot be None if 'utc_end' "
                         "is specified")

    if utc_end is None and utc_start is not None:
        utc_end = datetime.datetime.today()

    utc_start = _check_date(utc_start)
    utc_end = _check_date(utc_end)

    if utc_start is None and utc_end is None:
        return None
    else:
        return utc_start + '/' + utc_end


def _check_pollutant(pollutant):
    """Check if valid pollutant or convert short form """

    if pollutant not in POLLUTANTS:
        try:
            pollutant = SAROAD_CODE[pollutant]
        except KeyError:
            raise ValueError("Pollutant '{0}' not recognized".format(pollutant))

    return pollutant


def _process_sos_kwargs(pollutant=None, station=None, utc_start=None,
                        utc_end=None):
    """Convert arguments to correct form for SOS service"""

    # check pollutant
    if not isinstance(pollutant, list):
        pollutant = [pollutant]

    pollutant = [_check_pollutant(pol) for pol in pollutant]

    # check station
    if isinstance(station, list):
        station = ','.join(station)

    # check start and end
    period = _check_start_end(utc_start, utc_end)

    return pollutant, station, period


def query_ircelsos(pol, station=None, utc_start=None, utc_end=None):
    """
    Parameters
    ----------
    pol : str or list of str
    station : str of list of str, optional
        The station id(s). If not specified, query for all stations
        for which data are available for given pollutant.
    utc_start, utc_end : datetime.datetime or string, optional
        If both are None, query entire availabe time period.

    Returns
    -------
    response : string
    """

    pol, station, period = _process_sos_kwargs(
        pol, station, utc_start, utc_end)

    offerings = pol
    observedProperties = pol
    responseFormat = 'text/xml;subtype="om/1.0.0"'
    kwds = {}
    if station:
        kwds['featureofinterest'] = station
    kwds['eventTime'] = period

    response = SOS.get_observation(
        offerings=offerings, responseFormat=responseFormat,
        observedProperties=observedProperties, **kwds)

    return response


#response = query_ircelsos('o3', 'BETN060', '2015-03-27T00:00:00', '2015-03-27T10:00:00')
