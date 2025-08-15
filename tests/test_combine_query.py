import unittest
from datetime import datetime
from nrl.combine_query import CombineQuery


class TestCombineQuery(unittest.TestCase):
    def setUp(self):
        self.combine_query = CombineQuery()
        self.base_url = "combine?"

    def test_build_query_with_element_manufacturer_model(self):
        # Test with element, manufacturer, and model
        params = {
            'element': 'sensor',
            'manufacturer': 'EQMet',
            'model': 'CMG*',
            'format': 'resp'
        }
        query = self.combine_query.build_query(params)
        self.assertIn("element=sensor", query)
        self.assertIn("manufacturer=EQMet", query)
        self.assertIn("model=CMG*", query)
        self.assertIn("format=resp", query)

    def test_build_query_with_instconfig(self):
        # Test with instconfig
        params = {
            'instconfig': 'datalogger_EQMet_SMA_PG1_FR50',
            'format': 'stationxml'
        }
        query = self.combine_query.build_query(params)
        self.assertIn("instconfig=datalogger_EQMet_SMA_PG1_FR50", query)
        self.assertIn("format=stationxml", query)

    def test_build_query_with_epoch(self):
        # Test with epoch parameters
        epoch_params = {
            'network': 'IU',
            'station': 'ANMO',
            'location': '00',
            'channel': 'BHZ',
            'start_time': datetime(2020, 1, 1),
            'end_time': datetime(2021, 1, 1)
        }
        params = {
            'element': 'sensor',
            'epoch': epoch_params,
            'format': 'resp'
        }
        query = self.combine_query.build_query(params)
        self.assertIn("net=IU", query)
        self.assertIn("sta=ANMO", query)
        self.assertIn("loc=00", query)
        self.assertIn("cha=BHZ", query)
        self.assertIn("starttime=2020-01-01T00:00:00", query)
        self.assertIn("endtime=2021-01-01T00:00:00", query)

    def test_error_handling(self):
        # Test with no required parameters
        self.combine_query.set_error_handler(False)
        with self.assertRaises(ValueError):
            self.combine_query.build_query({'format': 'resp'})

        # Test with invalid element
        with self.assertRaises(ValueError):
            self.combine_query.build_query({'element': 'invalid_element'})

        # Test with error handler ignoring invalid element
        self.combine_query.set_error_handler(True)
        query = self.combine_query.build_query({'element': 'invalid_element',
                                                'manufacturer': 'test'})
        self.assertNotIn("element=invalid_element", query)

    def test_case_insensitivity(self):
        # Test case-insensitivity for element
        params = {
            'element': 'Datalogger',
            'manufacturer': 'EQMet',
            'model': 'SMA',
            'format': 'resp'
        }
        query = self.combine_query.build_query(params)
        self.assertIn("element=Datalogger", query)


if __name__ == '__main__':
    unittest.main()
