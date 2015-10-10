# -*- coding: utf-8 -*-
"""
Metadata about stations and pollutants for this sos.

@author: Joris Van den Bossche
"""

from . import SOS
from ._stations import STATIONS

contents = SOS.contents

POLLUTANTS = {key: {'id': contents[key].id,
                    'name': contents[key].name,
                    'features_of_interest': contents[key].features_of_interest}
              for key in contents}

# update stations with measured pollutants
for st in STATIONS:
    pols = []
    for pol in POLLUTANTS:
        if st in POLLUTANTS[pol]['features_of_interest']:
            pols.append(POLLUTANTS[pol]['id'])
    STATIONS[st]['offerings'] = pols

STATION_LOCAL_CODES = {STATIONS[code]['name']: STATIONS[code]['id']
                       for code in STATIONS}

SAROAD_CODE = {'o3': '44201 - O3',
               'no2': '42602 - NO2',
               'pm10': '81102 - PM10',
               'pm25': '81104 - PM2.5',
               'so2': '42401 - SO2',
               'co': '42101 - CO',
               'bc': '16111 - Black Carbon'}
