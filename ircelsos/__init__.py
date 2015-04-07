# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 23:11:39 2015

@author: Joris Van den Bossche
"""


def main():
    import sys
    from query_ircelsos import query_ircelsos
    from sosparser import get_observations, parse_observation

    pol = sys.argv[1]
    station = sys.argv[2]
    utc_start = sys.argv[3]
    utc_end = sys.argv[4]

    response = query_ircelsos(pol, station, utc_start, utc_end)
    observations = get_observations(response)

    for obs in observations:
        st_info, raw_data = parse_observation(obs)

        with file('{0}_{1}.csv'.format(pol, station), 'w') as f:
            f.writelines(raw_data.replace(';', '\n'))
