from math import pi
from ColorController.helpers import *
import warnings


def invert_rgb(r, g, b):
    """
    Returns the inverse of r, g, b, where r, g, b are each values in range(0,256).
    """
    if any(ch < 0 or ch > 255 for ch in [r, g, b]):
        raise ValueError(f"Inputs for r, g, and b must be integer values between 0 and 255. "
                         f"You entered values {r, g, b} for (r, g, b)")
    if (type(r), type(g), type(b)) != (int, int, int):
        warnings.warn(f"Inputs for r, g, and b must be integer values between 0 and 255. "
                      f"You entered types {(type(r), type(g), type(b))} for (r, g, b)")
    r = 255 - r
    g = 255 - g
    b = 255 - b
    return r, g, b


def rgb_to_hex(red, green, blue):
    """
    Return color as #rrggbb for the given color values. Does not handle unbounded values (bigger than 255).
    """
    if any(ch < 0 or ch > 255 for ch in [red, green, blue]):
        raise ValueError(f"Inputs for red, green, and blue must be integer values between 0 and 255. "
                         f"You entered values {red, green, blue} for (red, green, blue)")
    if (type(red), type(green), type(blue)) != (int, int, int):
        warnings.warn(f"Inputs for red, green, and blue must be integer values between 0 and 255. "
                      f"You entered types {(type(red), type(green), type(blue))} for (r, g, b)")
    return '#%02x%02x%02x' % (int(round(red)), int(round(green)), int(round(blue)))


def hex_to_rgb(hex_str=str):
    """
    Return (red, green, blue) for the color given as #rrggbb. Values are integers only, as they should be.
    """
    hex_str = hex_str.lstrip('#')
    len_hex = len(hex_str)
    if len_hex != 6:
        raise ValueError('Hex code must be 6 digits long.')
    return tuple(int(hex_str[i:i + len_hex // 3], 16) for i in range(0, len_hex, len_hex // 3))


def colorsys_hsv_to_hsv360(colorsys_hsv=tuple):
    """
    Takes an HSV triplet as provided by colorsys, and converts it to match the
    notation used in colornames.txt
    """
    h = colorsys_hsv[0] * 360
    s = colorsys_hsv[1] * 100
    v = (colorsys_hsv[2] / 255) * 100
    return regular_round(h), regular_round(s), regular_round(v)


def hsv360_to_hsvdistance(hsv360=tuple):
    """
    Takes an HSV triplet as provided by colorsys_hsv_to_hsv360(), and converts it to match the
    notation used in the function for calculating distance between colors.
    """
    new_h = (hsv360[0] / 360) * (2 * pi)
    new_s = hsv360[1] / 100
    new_v = hsv360[2] / 100
    return new_h, new_s, new_v
