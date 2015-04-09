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
                        help='Station number. If no provided, use all available'
                        ' stations for that pollutant')
    parser.add_argument('--period', '-p', type=str, nargs=2,
                        help='Period of the measurements given as "start stop"')
    args = parser.parse_args()

    from query_ircelsos import query_ircelsos
    from sosparser import get_observations, parse_observation

    pollutant = args.pollutant
    if args.station:
        station = args.station[0]
    else:
        station = None
    response = query_ircelsos(pollutant, station, args.period[0],
                              args.period[1])
    observations = get_observations(response)

    for obs in observations:
        st_info, raw_data = parse_observation(obs)

        with file('{0}_{1}.csv'.format(pollutant, st_info['name']), 'w') as f:
            f.writelines(raw_data.replace(';', '\n'))
