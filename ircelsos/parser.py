# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 21:41:22 2015

@author: Joris Van den Bossche

Functionality for parsing the returned XML.
"""

#import os
import io
import xml.etree.ElementTree as ET


def get_observations(response):
    """
    Extract the Observation elements from the ObservationCollection.

    Returns
    -------
    observations : list

    """

    if isinstance(response, bytes):
        response = io.BytesIO(response)
    elif isinstance(response, str):
        response = io.StringIO(response)

    #tree = ET.parse('temp.xml')
    tree = ET.parse(response)

    root = tree.getroot()

    assert root.tag == '{http://www.opengis.net/om/1.0}ObservationCollection'

    members = root.findall('{http://www.opengis.net/om/1.0}member')

    observations = []

    for member in members:
        observations += list(member)

    return observations

#obs = observations[0]


def parse_observation(obs):
    """
    Parse the Observation element: extract the featureOfInterest
    information into `st_info` and the values from the result -
    DataArray into `raw_data`.

    Returns
    -------
    st_info, raw_data
    """

    assert obs.tag == '{http://www.opengis.net/om/1.0}Observation'

    obs_info = {}

    ## decode the sampling time

    samplingtime = obs.findall('{http://www.opengis.net/om/1.0}samplingTime')
    period = samplingtime[0].find('{http://www.opengis.net/gml}TimePeriod')
    begin = period.find('{http://www.opengis.net/gml}beginPosition').text
    end = period.find('{http://www.opengis.net/gml}endPosition').text
    obs_info['sampling_time'] = [begin, end]

    ## decode the feature information

    feat = obs.findall('{http://www.opengis.net/om/1.0}featureOfInterest')

    if len(feat) != 1:
        raise Exception('no/more than one om:featureOfInterest')

    point = feat[0].findall('{http://www.opengis.net/sampling/1.0}SamplingPoint')

    if len(point) != 1:
        raise Exception('no/more than one sa:SamplingPoint')

    try:
        point = point[0]
        st_info = {}
        st_info['description'] = point.find('{http://www.opengis.net/gml}description').text
        st_info['long_name'] = point.find('{http://www.opengis.net/gml}name').text
        name, _ = st_info['long_name'].split(' - ')
        st_info['name'] = name
        st_info['id'] = point.attrib['{http://www.opengis.net/gml}id']
    except:
        raise

    obs_info['feature_of_interest'] = st_info

    ## decode the data array values

    result = obs.findall('{http://www.opengis.net/om/1.0}result')
    if len(result) != 1:
        raise Exception('no/more than one om:result')

    data = result[0].findall('{http://www.opengis.net/swe/1.0.1}DataArray')
    if len(data) != 1:
        raise Exception('no/more than one swe:DataArray')

    ## decode components and encoding

    values = data[0].findall('{http://www.opengis.net/swe/1.0.1}values')
    if len(values) != 1:
        raise Exception('no/more than one swe:values')

    raw_data = values[0].text

    return obs_info, raw_data

#st_info, raw_data = parse_observation(obs)
#
#split()
#
#with file('test.csv', 'w') as f:
#    f.writelines(raw_data.replace(';', '\n'))
