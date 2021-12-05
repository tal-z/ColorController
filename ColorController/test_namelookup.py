import unittest
from ColorController.namelookup import measure_hsv_distance, query_hex_codes, find_closest_color_names


class TestNameLookup(unittest.TestCase):
    #def test_measure_hsv_distance(self):
        #self.assertEqual(True, True)  # add assertion here

    def test_query_hex_codes(self):
        self.assertTrue(("#FF0000" in query_hex_codes('red')))
        self.assertTrue(("#000000" in query_hex_codes('black')))
        self.assertTrue(("#FFFFFF" in query_hex_codes('white')))

    #def test_find_closest_color_names(self):
        #self.assertEqual(True, True)  # add assertion here

