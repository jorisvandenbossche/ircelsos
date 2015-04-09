# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 23:11:39 2015

@author: Joris Van den Bossche
"""


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='ircelsos',
        description='Download air quality data from the SOS of IRCEL - CELINE.')

    parser.add_argument('pollutant',
                        help='The pollutant')
    parser.add_argument('--station', '-s', nargs=1,
                        help='Station number')
    parser.add_argument('--period', '-p', type=str, nargs=2,
                        help='Period of the measurements given as "start stop"')
    args = parser.parse_args()

    from query_ircelsos import query_ircelsos
    from sosparser import get_observations, parse_observation
    response = query_ircelsos(args.pollutant, args.station[0], args.period[0],
                              args.period[1])
    observations = get_observations(response)

    for obs in observations:
        st_info, raw_data = parse_observation(obs)

        with file('{0}_{1}.csv'.format(pol, station), 'w') as f:
            f.writelines(raw_data.replace(';', '\n'))
