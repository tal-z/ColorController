import os
import pandas as pd
import sqlite3
from math import sin, cos
from ColorController.conversions import hex_to_rgb, colorsys_hsv_to_hsv360, hsv360_to_hsvdistance
import colorsys

CURRENT_DIR = os.path.dirname(__file__)

with sqlite3.connect(r'ColorController/colornames.db') as con:
    cur = con.cursor()

sql = """
    SELECT * FROM colors
"""

colors_df = pd.read_sql(sql, con)
for col in colors_df.columns:
    if type(colors_df[col][0]) == str and colors_df[col][0][0] == '(':
        colors_df[col] = colors_df[col].apply(lambda x: x.lstrip("(").rstrip(")"))
        colors_df[[*[f"{letter}_{col}" for letter in col]]] = colors_df[col].str.split(",", expand=True)

colors_df = colors_df[
    ['index', 'NAME', 'RGB', 'R_RGB', 'G_RGB', 'B_RGB', 'HEX', 'HSV', 'H_HSV', 'S_HSV', 'V_HSV',
       'XYZ', 'X_XYZ', 'Y_XYZ', 'Z_XYZ', 'LAB', 'L_LAB', 'A_LAB', 'B_LAB', 'LCH', 'L_LCH', 'C_LCH', 'H_LCH',
       'CMYK', 'C_CMYK', 'M_CMYK', 'Y_CMYK', 'K_CMYK', 'NEIGHBOUR_STR', 'NUM_NEIGHBOURS_MAXDE',
       'WORD_TAGS']
]
colors_df.columns = ['index', 'NAME', 'RGB', 'R_RGB', 'G_RGB', 'B_RGB', 'HEX', 'HSV', 'h', 's', 'v',
       'XYZ', 'X_XYZ', 'Y_XYZ', 'Z_XYZ', 'LAB', 'L_LAB', 'A_LAB', 'B_LAB', 'LCH', 'L_LCH', 'C_LCH', 'H_LCH',
       'CMYK', 'C_CMYK', 'M_CMYK', 'Y_CMYK', 'K_CMYK', 'NEIGHBOUR_STR', 'NUM_NEIGHBOURS_MAXDE',
       'WORD_TAGS']





def measure_hsv_distance(hsv1=tuple, hsv2=tuple):
    """
    Read this: https://stackoverflow.com/questions/35113979/calculate-distance-between-colors-in-hsv-space
    """
    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2
    distance = ((sin(h1) * s1 * v1 - sin(h2) * s2 * v2) ** 2
                + (cos(h1) * s1 * v1 - cos(h2) * s2 * v2) ** 2
                + (v1 - v2) ** 2)
    return distance


def query_hex_codes(token=str):
    """
    Takes a color name, and checks whether it is present in a pre-defined dictionary of color names.
    If the name is found, it returns the full range of hex codes that match the color name.
    """
    token = token.replace(" ", "_").lower()
    if token in colors_df.NAME.values:
        return sorted(list(colors_df.query(f'NAME=="{token.lower()}"').HEX))
    else:
        raise KeyError(f"Color name '{token}' not found in colornames.txt")


def find_closest_color_names(hex_str=str):
    """
    Calculates distance between a given color hex code and every color in the colornames.txt database,
    and returns the a list of the closest color names.
    Only returns multiple results if there is a tie for the closest color.
    """
    r, g, b = hex_to_rgb(hex_str)
    h1, s1, v1 = colorsys.rgb_to_hsv(r, g, b)
    h1, s1, v1 = colorsys_hsv_to_hsv360((h1, s1, v1))
    h1, s1, v1 = hsv360_to_hsvdistance((h1, s1, v1))

    closenames_df = pd.DataFrame(colors_df)
    closenames_df['hsv'] = [(h, s, v) for h, s, v in
                            zip(closenames_df['h'], closenames_df['s'], closenames_df['v'])]
    closenames_df['hsv'] = closenames_df['hsv'].apply(hsv360_to_hsvdistance)
    closenames_df['distance'] = closenames_df['hsv'].apply(lambda x: measure_hsv_distance((h1, s1, v1), x))

    closest_distance = closenames_df.sort_values(by='distance').iloc[0].distance

    return sorted(list(set(closenames_df[closenames_df['distance'] == closest_distance].NAME)))
