# -*- coding: utf-8 -*-
"""
Pandas interface

"""

import six

if six.PY3:
    from io import StringIO
else:
    from StringIO import StringIO

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def query(pollutant, station=None, utc_start=None, utc_end=None):
    """
    Download air quality data from the SOS of IRCEL-CELINE.

    Parameters
    ----------
    pollutant : str
        The pollutant.
    station : str or list of str, default None
        The stations for which to download the data. If none is given,
        use all available stations for that pollutant.
    utc_start, utc_end : str, datetime
        Period of the measurements to download. If not provided,
        download entire available period. If no end date is given,
        download the data up to now.

    Returns
    -------
    pandas DataFrame

    """
    from .query_ircelsos import query_ircelsos
    from .parser import get_observations, parse_observation

    if not HAS_PANDAS:
        raise ImportError("pandas is required for interactive usage")

    response = query_ircelsos(pollutant, station, utc_start, utc_end)
    observations = get_observations(response)
    if not observations:
        raise ValueError('No observations found')

    obs_df = []

    for obs in observations:
        st_info, raw_data = parse_observation(obs)
        df = pd.read_csv(StringIO(raw_data), lineterminator=';', index_col=0,
                         names=['time', st_info['feature_of_interest']['name']])
        obs_df.append(df)

    return pd.concat(obs_df, axis=1)
