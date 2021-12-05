import colorsys
import unittest
from math import pi

from ColorController.conversions import rgb_to_hex, hex_to_rgb, invert_rgb, colorsys_hsv_to_hsv360, hsv360_to_hsvdistance


class TestConversions(unittest.TestCase):

    def test_invert_rgb(self):
        self.assertEqual(invert_rgb(255, 255, 255), (0, 0, 0))
        self.assertEqual(invert_rgb(0, 0, 0), (255, 255, 255))
        self.assertWarns(UserWarning, invert_rgb, 100, 25.5, 30)
        self.assertRaises(ValueError, invert_rgb, 100, 25.5, 500)
        self.assertRaises(ValueError, invert_rgb, 100, 25.5, -3)
        with self.assertRaises(ValueError) as context:
            invert_rgb(100, 255, -30)
        self.assertTrue(f"Inputs for r, g, and b must be integer values between 0 and 255. "
                        f"You entered values (100, 255, -30) for (r, g, b)" in str(context.exception)
                        )

    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex(0, 0, 0), '#000000')
        self.assertEqual(rgb_to_hex(255, 255, 255), '#ffffff')
        self.assertEqual(rgb_to_hex(0, 0, 1), '#000001')
        self.assertEqual(rgb_to_hex(1, 1, 1), '#010101')
        self.assertEqual(rgb_to_hex(5, 30, 255), '#051eff')
        self.assertEqual(rgb_to_hex(5.0, 29.9999, 255), '#051eff')
        self.assertEqual(rgb_to_hex(5.0, 30.0001, 255), '#051eff')
        self.assertWarns(UserWarning, rgb_to_hex, 200.1, 20, 90.5)
        self.assertRaises(ValueError, rgb_to_hex, 200, -30, 100)
        with self.assertRaises(ValueError) as context:
            rgb_to_hex(500, 30.1, 255.01)
        self.assertTrue(f"Inputs for red, green, and blue must be integer values between 0 and 255. "
                        f"You entered values (500, 30.1, 255.01) for (red, green, blue)" in str(context.exception)
                        )

    def test_hex_to_rgb(self):
        self.assertEqual(hex_to_rgb('#000000'), (0, 0, 0))
        self.assertEqual(hex_to_rgb('#FFFFFF'), (255, 255, 255))
        self.assertEqual(hex_to_rgb('0c2526'), (12, 37, 38))
        self.assertEqual(hex_to_rgb('#85d849'), (133, 216, 73))
        self.assertEqual(hex_to_rgb('2A918A'), (42, 145, 138))
        self.assertRaises(ValueError, hex_to_rgb, '2A9181b')
        with self.assertRaises(ValueError) as context:
            hex_to_rgb('12345')
        self.assertTrue('Hex code must be 6 digits long.' in str(context.exception))

    def test_colorsys_hsv_to_hsv360(self):
        self.assertEqual(colorsys_hsv_to_hsv360((0, 0, 255)), (0, 0, 100))
        self.assertEqual(colorsys_hsv_to_hsv360((1, 1, 255)), (360, 100, 100))
        self.assertEqual(colorsys_hsv_to_hsv360((.25, .25, 100)), (90, 25, int(100 / 2.55)))

    def test_hex_to_hsv360(self):
        r, g, b = hex_to_rgb('#F4ED7C')
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, s, v = colorsys_hsv_to_hsv360((h, s, v))
        self.assertEqual((h, s, v), (57, 49, 96))
        r, g, b = hex_to_rgb('4d8914')
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, s, v = colorsys_hsv_to_hsv360((h, s, v))
        self.assertEqual((h, s, v), (91, 85, 54))
        r, g, b = hex_to_rgb('#344ea3')
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, s, v = colorsys_hsv_to_hsv360((h, s, v))
        self.assertEqual((h, s, v), (226, 68, 64))
        r, g, b = hex_to_rgb('211123')
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h, s, v = colorsys_hsv_to_hsv360((h, s, v))
        self.assertEqual((h, s, v), (293, 51, 14))

    def test_hsv360_to_hsvdistance(self):
        """
        Takes an HSV triplet as provided by colorsys_hsv_to_hsv360(), and converts it to match the
        notation used in the function for calculating distance between colors.
        """
        self.assertEqual(hsv360_to_hsvdistance((360, 100, 100)), (2*pi, 1, 1))
        self.assertEqual(hsv360_to_hsvdistance((360, 10, 10)), (2*pi, .1, .1))
        self.assertEqual(hsv360_to_hsvdistance((180, 10.05, 10)), (pi, .1005, .1))


