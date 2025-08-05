"""
This script shows how to use the library in different scenarios. The goal is
cover as many different cases as possible.
"""
from pathlib import Path
from nrl.NRLQuery import NRLQuery
from nrl.catalog_query import CatalogQuery
from datetime import datetime

default_download_folder = (Path(__file__).parent.resolve() / 'dl_test_folder')

# Test Prefix-lookup query
catalog_query = CatalogQuery()
catalog_query.set_error_handler(False)
nrl = NRLQuery()
nrl.set_error_handler(False)

# Create a couple of queries
catalog_prop_element_one = {
    'element': ['*'],
    'manufacturer': ['EQMet'],
    'model': ['SMA', '*'],
    'level': 'element',
    'updated_since': datetime(2019, 1, 6, 15, 8,
                              24, 78915),
    'format': 'xml',
    'nodata': 404
}

catalog_prop_element_two = {
    'element': [],
    'manufacturer': ['EQMet'],
    'model': ['SMA', '*'],
    'level': 'element',
    'updated_since': datetime(2018, 1, 6, 15, 8,
                              24, 78915),
    'format': 'json',
    'nodata': 404
}

catalog_prop_element_three = {
    'element': [],
    'manufacturer': [],
    'model': [],
    'level': 'configuration',
    'format': 'xml',
    'nodata': 404
}

catalog_prop_element_four = {
    'element': [],
    'level': 'model',
    'format': 'xml',
    'nodata': 404
}

catalog_prop_element_five = {
    'element': ['Datalogger', 'sensor'],
    'level': 'configuration',
    'format': 'text',
    'nodata': 404,
    'updated_since': datetime(2018, 1, 6, 15, 8,
                              24, 78915)
}

# Right now if you send a bad request to the library you will receive an error
# message and the process gets terminated. Need to modify the library to
# handle errors in a better way. Like not terminating the process all together
catalog_prop_element_six = {
    'element': ['badelement'],
    'manufacturer': ['EQMet'],
    'model': ['SMA', ''],
    'level': 'configuration',
    'updated_since': datetime(2018, 1, 6, 15, 8,
                              24, 78915),
    'format': 'text',
    'nodata': 404
}


# Case one
catalog_prop_response_one = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_one)

NRLQuery.write_to_file(response=catalog_prop_response_one,
                       dl_path=default_download_folder)

# Case two
catalog_prop_response_two = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_two)

NRLQuery.write_to_file(response=catalog_prop_response_two,
                       dl_path=default_download_folder)

# Case three
catalog_prop_response_three = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_three)

NRLQuery.write_to_file(response=catalog_prop_response_three,
                       dl_path=default_download_folder)

# Case four
catalog_prop_response_four = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_four)

NRLQuery.write_to_file(response=catalog_prop_response_four,
                       dl_path=default_download_folder)

# Case five
catalog_prop_response_five = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_five)

NRLQuery.write_to_file(response=catalog_prop_response_five,
                       dl_path=default_download_folder)

nrl.set_error_handler(True)

# Case six - bad request
catalog_prop_element_six = nrl.nrl_query(
    query_type='catalog', nrl_query_property=catalog_prop_element_six)
NRLQuery.write_to_file(response=catalog_prop_element_six,
                       dl_path=default_download_folder)