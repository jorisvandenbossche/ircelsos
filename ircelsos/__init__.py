# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 23:11:39 2015

@author: Joris Van den Bossche
"""


from .sos import get_sos

SOS = get_sos()


try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def query(pollutant, station=None, utc_start=None, utc_end=None):
    """
    Download air quality data from IRCEL-CELINE





    """

    if not HAS_PANDAS:
        raise ImportError("pandas is required for interactive usage")

    from StringIO import StringIO
    from .query_ircelsos import query_ircelsos
    from .parser import get_observations, parse_observation

    response = query_ircelsos(pollutant, station, utc_start, utc_end)
    observations = get_observations(response)
    if not observations:
        raise ValueError('No observations found')

    obs_df = []

    for obs in observations:
        st_info, raw_data = parse_observation(obs)
        df = pd.read_csv(StringIO(raw_data), lineterminator=';',
                         names=['time', st_info['id']], index_col=0)
        obs_df.append(df)

    return pd.concat(obs_df, axis=1)
