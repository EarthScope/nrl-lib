""" Test the catalog_query module."""

import unittest
from datetime import datetime
from nrl.catalog_query import CatalogQuery


class TestCatalogQuery(unittest.TestCase):
    """ Test PrefixLookupQuery class."""
    def setUp(self):
        """ Set up test fixtures, if any"""
        self.catalog_query = CatalogQuery()

    def test_build_query_correct_input(self):
        params = {
            'element': ['sensor', 'datalogger'],
            'manufacturer': ['WQMet'],
            'model': ['SMA'],
            'level': 'configuration',
            'updated_since': datetime(2024, 3, 12),
            'format': 'xml',
            'nodata': 404
        }
        query = self.catalog_query.build_query(params)
        self.assertIn("element=sensor,datalogger", query)
        self.assertIn("manufacturer=WQMet", query)
        self.assertIn("model=SMA", query)
        self.assertIn("level=configuration", query)
        self.assertIn("updatedsince=2024-03-12", query)
        self.assertIn("format=xml", query)
        self.assertIn("nodata=404", query)

    def test_error_handling(self):
        self.catalog_query.set_error_handler(False)

        # Test with invalid element
        with self.assertRaises(ValueError):
            self.catalog_query.build_query({'element': ['invalid_element']})

        # Test with invalid level
        with self.assertRaises(ValueError):
            self.catalog_query.build_query({'level': 'invalid_level',
                                            'element': ['sensor']})

    def test_error_handling_ignore(self):
        self.catalog_query.set_error_handler(True)

        # Test with invalid element and error handler ignoring it
        query = self.catalog_query.build_query({'element': ['invalid_element',
                                                            'sensor']})
        self.assertNotIn("invalid_element", query)
        self.assertIn("element=sensor", query)

        # Test with invalid level and error handler using default
        query = self.catalog_query.build_query({'level': 'invalid_level',
                                                'element': ['sensor']})
        self.assertIn("level=configuration", query)

    def test_case_insensitivity(self):
        # Test case-insensitivity for element
        params = {
            'element': ['Sensor', 'Datalogger'],
            'level': 'Configuration',
            'format': 'XML'
        }
        query = self.catalog_query.build_query(params)
        self.assertIn("element=Sensor,Datalogger", query)
        self.assertIn("level=configuration", query)
        self.assertIn("format=xml", query)

    def test_missing_parameters(self):
        # Test with missing optional parameters
        params = {
            'element': ['sensor'],
            'format': 'json'
        }
        query = self.catalog_query.build_query(params)
        self.assertIn("element=sensor", query)
        self.assertIn("format=json", query)
        self.assertIn("level=configuration", query)  # Default value
        self.assertNotIn("manufacturer", query)
        self.assertNotIn("model", query)
        self.assertNotIn("updatedsince", query)


if __name__ == '__main__':
    unittest.main()
