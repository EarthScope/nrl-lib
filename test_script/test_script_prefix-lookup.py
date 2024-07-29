"""
This script shows how to use the library in different scenarios. The goal is
cover as many different cases as possible.
"""
from pathlib import Path, PurePath
from nrl.NRLQuery import NRLQuery
from nrl.prefix_lookup_query import PrefixLookupQuery

default_download_folder = (Path(__file__).parent.resolve() / 'dl_test_folder')
# print(Path(__file__).parent.resolve())
# print(default_download_folder)
# Test Prefix-lookup query
prefix_lookup_query = PrefixLookupQuery()

# Create a dictionary to pass the information needed for prefix-lookup query
prefix_prop_404_xml = {'nodata': 404, 'format': 'xml'}
prefix_prop_204_json = {'nodata': 204, 'format': 'json'}
prefix_prop_404_text = {'nodata': 404, 'format': 'text'}

# Use the NRLQuery class to submit your query to the NRL web service
nrl = NRLQuery()
# Test 1
prefix_prop_204_json_response = nrl.nrl_query(
    query_type='prefix-lookup', nrl_query_property=prefix_prop_204_json)
NRLQuery.write_to_file(response=prefix_prop_204_json_response,
                       dl_path=default_download_folder)
# Test 2
prefix_prop_404_xml_response = nrl.nrl_query(
    query_type='prefix-lookup',nrl_query_property=prefix_prop_404_xml)
NRLQuery.write_to_file(response=prefix_prop_404_xml_response,
                       dl_path=default_download_folder)

# Test 3
prefix_prop_404_text_response = nrl.nrl_query(
    query_type='prefix-lookup', nrl_query_property=prefix_prop_404_text)
NRLQuery.write_to_file(response=prefix_prop_404_text_response,
                       dl_path=default_download_folder)

# # Let's have some mistake in using the library and prefix lookup
prefix_prop_404_text_bad_keys = {'nodata': 404, 'outformat': 'text'}
prefix_prop_404_text_bad_keys_response = nrl.nrl_query(
    query_type='prefix-lookup',
    nrl_query_property=prefix_prop_404_text_bad_keys)
NRLQuery.write_to_file(response=prefix_prop_404_text_bad_keys_response,
                       dl_path=default_download_folder)

