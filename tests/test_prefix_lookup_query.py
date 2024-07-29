# -*- coding: utf-8 -*-

""" Test the prefix_lookup_query module."""

import unittest
from nrl.prefix_lookup_query import PrefixLookupQuery, PrefixLookupProperty

CORRECT_OUTPUT = 'prefix-lookup?format=xml&nodata=404'


class TestPrefixLookupQuery(unittest.TestCase):
    """ Test PrefixLookupQuery class."""
    def setUp(self):
        """ Set up test fixtures, if any"""
        self.property = PrefixLookupProperty()
        self.wrong_input_dict_size = dict(format='xml', nodata=404, url='')
        self.wrong_format_input = dict(format='lmx', nodata=404)
        self.wrong_nodata_input = dict(format='xml', nodata=102)
        self.correct_input = dict(format='xml', nodata=404)

    def test_build_query(self):
        """ Test build_query method"""
        prefix_lookup = PrefixLookupQuery()
        # correct input
        output = prefix_lookup.build_query(self.correct_input)
        self.assertEqual(output, CORRECT_OUTPUT)

        # Incorrect input size
        with (self.assertRaises(ValueError)):
            prefix_lookup.build_query(self.wrong_input_dict_size)

        # Incorrect input for format
        output = prefix_lookup.build_query(self.wrong_format_input)
        self.assertEqual(output, CORRECT_OUTPUT)

        # Incorrect input for nodata
        output = prefix_lookup.build_query(self.wrong_nodata_input)
        self.assertEqual(output, CORRECT_OUTPUT)
