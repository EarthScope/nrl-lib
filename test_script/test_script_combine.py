"""
This script shows how to use the library in different scerarios. The goal is
cover as many different cases as possible.
"""
from pathlib import Path
from nrl.NRLQuery import NRLQuery
from nrl.combine_query import CombineQuery
from datetime import datetime

default_download_folder = (Path(__file__).parent.resolve() / 'dl_test_folder')

# Test Prefix-lookup query
combine_query = CombineQuery()
nrl = NRLQuery()

# Create a couple of queries
combine_prop_one = {
    'instconfig': 'sensor_CEADASE_CPHM-500_LP1_PG8_SG2250_STgroundVel:datalogger_EQMet_SMA_FR50',
    'element': ['Datalogger'],
    'manufacturer': [],
    'model': [],
    'updated_since': datetime(2018, 1, 6),
    'format': 'resp',
    'nodata': 404,
    'epoch': {
        'network': 'IU',
        'station': 'ANMO',
        'location': '00',
        'channel': 'BHZ',
        'start_time': datetime(2018, 1, 6, 15, 8,
                               24, 78915),
        'end_time': datetime(2019, 1, 6, 15, 8,
                             24, 78915)
    }
}

combine_prop_two = {
    'instconfig': 'sensor_CEADASE_CPHM-500_LP1_PG8_SG2250_STgroundVel:datalogger_EQMet_SMA_FR50',
    'element': ['datalogger'],
    'manufacturer': [],
    'model': [],
    'updated_since': datetime(2018, 1, 6),
    'format': 'resp',
    'nodata': 204,
    'epoch': {
        'network': '',
        'station': '',
        'location': '',
        'channel': '',
        'start_time': '',
    }
}

combine_prop_three = {
    'element': ['datalogger', 'sensor'],
    'manufacturer': ['EQMet'],
    'model': ['SMA*'],
    'updated_since': datetime(2021, 1, 1),
    'format': 'resp.zip',
    'nodata': 404,
    'epoch': {
        'network': 'IU',
        'station': 'ANMO',
        'location': '00',
        'channel': 'BHZ',
        'start_time': datetime(2020, 1, 1),
        'end_time': datetime(2021, 1, 1)
    }
}

combine_prop_four = {
    'element': ['integrated', 'soh'],
    'manufacturer': ['*'],
    'model': [],
    'updated_since': datetime(2021, 1, 1),
    'format': 'stationxml.zip',
    'nodata': 404,
    'epoch': {
        'network': '',
        'station': '',
        'location': '',
        'channel': '',
        'start_time': datetime.now(),
        'end_time': datetime.now()
    }
}

# Case one
combine_prop_response_one = nrl.nrl_query(query_type='combine',
                                          nrl_query_property=combine_prop_one)
NRLQuery.write_to_file(response=combine_prop_response_one,
                       dl_path=default_download_folder)

# Case two
combine_prop_response_two = nrl.nrl_query(query_type='combine',
                                          nrl_query_property=combine_prop_two)
NRLQuery.write_to_file(response=combine_prop_response_two,
                       dl_path=default_download_folder)

# Case three
combine_prop_response_three = nrl.nrl_query(
    query_type='combine',nrl_query_property=combine_prop_three)
NRLQuery.write_to_file(response=combine_prop_response_three,
                       dl_path= default_download_folder)

# Case four
combine_prop_response_four = nrl.nrl_query(
    query_type='combine',nrl_query_property=combine_prop_four)
NRLQuery.write_to_file(response=combine_prop_response_four,
                       dl_path= default_download_folder)