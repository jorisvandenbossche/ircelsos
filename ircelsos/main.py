# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 23:11:39 2015

@author: Joris Van den Bossche
"""
from __future__ import print_function

from dateutil.parser import parse


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='ircelsos',
        description='Download air quality data from the SOS of IRCEL - CELINE.')
    subparsers = parser.add_subparsers(metavar='', dest='sub')

    query_parser = subparsers.add_parser(
        'query',
        description='Download air quality data from the SOS of IRCEL - CELINE.',
        help='Download air quality data')
    query_parser.add_argument(
        'pollutant', help='The pollutant')
    query_parser.add_argument(
        '--station', '-s', nargs=1,
        help='Station number. If no provided, use all available stations '
             'for that pollutant.')
    query_parser.add_argument(
        '--period', '-p', type=str, nargs=2, metavar=('START', 'STOP'),
        help='Period of the measurements given as "start stop". If not '
             'provided, download entire available period.')

    info_parser = subparsers.add_parser(
        'info',
        description='Get information on stations and pollutants available in the SOS of IRCEL - CELINE.',
        help='Get information on stations and pollutants')

    args = parser.parse_args()

    if args.sub == 'query':
        main_query(args)
    elif args.sub == 'info':
        main_info(args)


def main_query(args):

    from .query_ircelsos import query_ircelsos
    from .parser import get_observations, parse_observation

    print("SOS of IRCEL - CELINE")
    print("Downloading ...")

    pollutant = args.pollutant
    if args.station:
        station = args.station[0]
    else:
        station = None

    if args.period is None:
        start = None
        end = None
    else:
        start, end = args.period

    response = query_ircelsos(pollutant, station, start, end)
    observations = get_observations(response)
    if not observations:
        print('No observations found')
        import sys
        sys.exit()

    for obs in observations:
        obs_info, raw_data = parse_observation(obs)

        filename = '{0}_{1}_{2}_{3}.csv'.format(
            pollutant, obs_info['feature_of_interest']['name'],
            parse(obs_info['sampling_time'][0]).strftime('%Y%m%d'),
            parse(obs_info['sampling_time'][1]).strftime('%Y%m%d'))
        print("Writing file '{}'".format(filename))
        with open(filename, 'w') as outfile:
            outfile.writelines(raw_data.replace(';', '\n'))


def main_info(args):

    print("SOS of IRCEL - CELINE")
