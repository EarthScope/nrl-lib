# -*- coding: utf-8 -*-

""" Test the prefix_lookup_query module."""

import unittest
from nrl.prefix_lookup_query import PrefixLookupQuery


class TestPrefixLookupQuery(unittest.TestCase):
    def setUp(self):
        self.prefix_lookup_query = PrefixLookupQuery()

    def test_build_query_correct_input(self):
        params = {'format': 'xml', 'nodata': 404}
        query = self.prefix_lookup_query.build_query(params)
        self.assertEqual(query, "prefix-lookup?format=xml&nodata=404")

        params_json = {'format': 'json', 'nodata': 204}
        query_json = self.prefix_lookup_query.build_query(params_json)
        self.assertEqual(query_json,
                         "prefix-lookup?format=json&nodata=204")

    def test_error_handling_strict(self):
        self.prefix_lookup_query.set_error_handler(False)

        # Test with invalid key
        with self.assertRaises(ValueError):
            self.prefix_lookup_query.build_query({'format': 'xml',
                                                  'invalid_key': 'value'})

        # Test with too many keys
        with self.assertRaises(ValueError):
            self.prefix_lookup_query.build_query({'format': 'xml',
                                                  'nodata': 404,
                                                  'extra': 'value'})

    def test_error_handling_ignore(self):
        self.prefix_lookup_query.set_error_handler(True)

        # Test with invalid key - should be ignored
        query = self.prefix_lookup_query.build_query({'format': 'xml',
                                                      'nodata': 404,
                                                      'invalid_key': 'value'})
        self.assertIn("format=xml", query)
        self.assertIn("nodata=404", query)

        # Test with invalid format value - should use default
        query_invalid_format = self.prefix_lookup_query.build_query({
            'format': 'invalid', 'nodata': 404})
        self.assertIn("format=xml", query_invalid_format)

        # Test with invalid nodata value - should use default
        query_invalid_nodata = self.prefix_lookup_query.build_query({
            'format': 'xml', 'nodata': 999})
        self.assertIn("nodata=404", query_invalid_nodata)

    def test_case_insensitivity(self):
        # Test case-insensitivity for format
        params = {'format': 'XML', 'nodata': 404}
        query = self.prefix_lookup_query.build_query(params)
        self.assertIn("format=xml", query)

    def test_defaults(self):
        # Test that default values are used when no parameters are provided
        query = self.prefix_lookup_query.build_query({})
        self.assertIn("format=xml", query)
        self.assertIn("nodata=404", query)


if __name__ == '__main__':
    unittest.main()
