""" Test the catalog_query module."""

import unittest
from nrl.catalog_query import CatalogQuery, CatalogProperty

CORRECT_OUTPUT = ('catalog?element=sensor,datalogger&manufacturer=WQMet&model='
                  'SMA&level=configuration&updatedsince=2024-03-12&format='
                  'xml&nodata=404')


class TestCatalogQuery(unittest.TestCase):
    """ Test PrefixLookupQuery class."""
    def setUp(self):
        """ Set up test fixtures, if any"""
        self.property = CatalogProperty()
        self.wrong_input_dict_size = dict(format='xml', nodata=404, url='')

        self.wrong_format_input = dict(element=['sensors', 'datalogger'],
                                       manufacturer=['WQMet'], model=['SMA'],
                                       level='configuration',
                                       updated_since='2024-03-12',
                                       format='lmx', nodata=404)

        self.wrong_nodata_input = dict(element=['sensors', 'datalogger'],
                                       manufacturer=['WQMet'], model=['SMA'],
                                       level='configuration',
                                       updated_since='2024-03-12',
                                       format='xml', nodata=100)

        self.wrong_element_input = dict(element=['sensors', 'datalogger'],
                                        manufacturer=['WQMet'], model=['SMA'],
                                        level='configuration',
                                        updated_since='2024-03-12',
                                        format='xml', nodata=404)

        self.wrong_level_input = dict(element=['sensor', 'datalogger'],
                                      manufacturer=['WQMet'], model=['SMA'],
                                      level='config',
                                      updated_since='2024-03-12',
                                      format='xml', nodata=404)

        self.correct_input = dict(element=['sensor', 'datalogger'],
                                  manufacturer=['WQMet'], model=['SMA'],
                                  level='configuration',
                                  updated_since='2024-03-12',
                                  format='xml', nodata=404)

    def test_build_query(self):
        """
        Test build_query
        :return: None
        """
        catalog_query = CatalogQuery()
        # Correct output
        out_put = catalog_query.build_query(self.correct_input)
        self.assertEqual(out_put, CORRECT_OUTPUT)

        # Incorrect element input
        with (self.assertRaises(ValueError)):
            catalog_query.build_query(self.wrong_element_input)

        # Incorrect input level
        with (self.assertRaises(ValueError)):
            catalog_query.build_query(self.wrong_level_input)

        # Incorrect format_input
        out_put = catalog_query.build_query(self.wrong_format_input)
        self.assertEqual(out_put, CORRECT_OUTPUT)

        # Incorrect nodata_input
        out_put = catalog_query.build_query(self.wrong_nodata_input)
        self.assertEqual(out_put, CORRECT_OUTPUT)
