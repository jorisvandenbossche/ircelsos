# -*- coding: utf-8 -*-
"""
Created on Wed Apr 07 21:41:22 2015

@author: Joris Van den Bossche
"""

#import os
import StringIO
import xml.etree.ElementTree as ET


#os.chdir("D:\PhD\github\ircelsos\ircelsos")


def get_observations(response):

    if isinstance(response, str):
        response = StringIO.StringIO(response)

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

    assert obs.tag == '{http://www.opengis.net/om/1.0}Observation'

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

    return st_info, raw_data

#st_info, raw_data = parse_observation(obs)
#
#split()
#
#with file('test.csv', 'w') as f:
#    f.writelines(raw_data.replace(';', '\n'))
