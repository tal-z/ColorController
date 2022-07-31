import os
import pandas as pd
from math import sin, cos
from ColorController.conversions import hex_to_rgb, colorsys_hsv_to_hsv360, hsv360_to_hsvdistance
import colorsys

CURRENT_DIR = os.path.dirname(__file__)

colors_df = pd.read_csv(os.path.join(CURRENT_DIR, 'colornames.txt'), delimiter=" ", skiprows=60, header=None)



colors_df.columns = ['IDX', 'NAME',
                     'rgb', 'R', 'G', 'B',
                     'hex', 'HEX',
                     'hsv', 'h', 's', 'v',
                     'xyz', 'X', 'Y', 'Z',
                     'lab', 'L', 'A', 'B',
                     'lch', 'L', 'C', 'H',
                     'cmyk', 'C', 'M', 'Y', 'K',
                     'NEIGHBOUR_STR', 'NUM_NEIGHBOURS_MAXDE', 'WORD_TAGS']
colors_df['WORD_TAGS'] = colors_df['WORD_TAGS'].apply(lambda x: x.split(":"))



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
