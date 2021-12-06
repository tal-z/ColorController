from ColorController.show_color import show_named_color, show_coded_color
from ColorController.conversions import rgb_to_hex, format_hsv, unlist, hex_to_rgb
from ColorController.namelookup import find_closest_color_names, query_hex_codes
import colorsys

class ColorController:

    def __init__(self, hex_code='', rgb=None, hsv=None, name=''):
        """Initializes class with one and only one of four optional attributes.
        If multiple attributes are passed, only one is used.
        The order of use is: hex_code, rgb, hsv, name.
        You should only pass one of these arguments upon initializing a new ColorController object.

        Example Inputs:
        hex_code --> '#ff0000'
        rgb --> (0, 255, 135)
        hsv --> (0.0, 1.0, 255)
        name --> 'maroon'
        """
        if hex_code:
            self._hex_code = hex_code
            self._rgb = hex_to_rgb(hex_code)
            red, green, blue = self._rgb
            h, s, v = colorsys.rgb_to_hsv(red, green, blue)
            self._hsv = format_hsv(h, s, v)
            self._name = find_closest_color_names(hex_code)
        elif rgb:
            red, green, blue = rgb
            self._hex_code = rgb_to_hex(red, green, blue)
            self._rgb = rgb
            h, s, v = colorsys.rgb_to_hsv(red, green, blue)
            self._hsv = format_hsv(h, s, v)
            self._name = find_closest_color_names(self._hex_code)
        elif hsv:
            h, s, v = hsv
            red, green, blue = colorsys.hsv_to_rgb(h, s, v)
            self._rgb = int(red), int(green), int(blue)
            self._hex_code = rgb_to_hex(red, green, blue)
            self._hsv = hsv
            self._name = find_closest_color_names(self._hex_code)
        elif name:
            self._hex_code = query_hex_codes(name)
            self._rgb = [hex_to_rgb(code) for code in self._hex_code]
            hsv_list = []
            for color in self._rgb:
                red, green, blue = color
                h, s, v = colorsys.rgb_to_hsv(red, green, blue)
                hsv_list.append(format_hsv(h, s, v))
            self._hsv = hsv_list
            self._name = name

    @property
    def name(self):
        """
        Because I want to auto-update values as they are called, I have selected to use "getters and setters,"
        implemented in Python as class properties. Class properties are themselves "decorators."
        This is the "getter" method, and it's job is to return the .name property.
        It works by  checking to see if there is a name set in the ._name attribute,
        and returns the name if there is. Because name is always set upon init, the check is redundant.
        """
        if self._name:
            return self._name

    @name.setter
    def name(self, new_name):
        """
        The decorator here is fairly clear that this is the "setter" method for the name property. When an instance of
        a ColorController object is provided with a new name property, this bit of code is responsible for updating all
        of the other properties. This is where the magic happens.
        """
        self._name = new_name
        self._hex_code = query_hex_codes(new_name)
        self._rgb = [hex_to_rgb(code) for code in self._hex_code]
        hsv_list = []
        for color in self._rgb:
            red, green, blue = color
            h, s, v = colorsys.rgb_to_hsv(red, green, blue)
            hsv_list.append(format_hsv(h, s, v))
        self._hsv = hsv_list

    @property
    def hex_code(self):
        """This is the hex_code getter.
        It works the same way as the name getter, but on hex_code."""
        if self._hex_code:
            return self._hex_code

    @hex_code.setter
    def hex_code(self, new_hex_code):
        """
        This is the hex_code setter. It also works the same as the name_setter.
        """
        self._hex_code = new_hex_code
        self._name = find_closest_color_names(new_hex_code)
        self._rgb = hex_to_rgb(new_hex_code)
        red, green, blue = self._rgb
        h, s, v = colorsys.rgb_to_hsv(red, green, blue)
        self._hsv = format_hsv(h, s, v)

    @property
    def rgb(self):
        """This is the rgb getter."""
        if self._rgb:
            return self._rgb

    @rgb.setter
    def rgb(self, new_rgb):
        """This is the rgb setter."""
        self._rgb = new_rgb
        red, green, blue = self._rgb
        self._name = find_closest_color_names(rgb_to_hex(red, green, blue))
        self._hex_code = rgb_to_hex(red, green, blue)
        h, s, v = colorsys.rgb_to_hsv(red, green, blue)
        self._hsv = format_hsv(h, s, v)

    @property
    def hsv(self):
        """This is the hsv getter."""
        if self._hsv:
            return self._hsv

    @hsv.setter
    def hsv(self, new_hsv):
        """This is the hsv setter. It has one extra step, because it is necessary
        to unpack the .hsv 3-tuple in order to convert back to rgb.
        """
        self._hsv = new_hsv
        h, s, v = new_hsv
        red, green, blue = colorsys.hsv_to_rgb(h, s, v)
        red, green, blue = int(red), int(green), int(blue)
        self._name = find_closest_color_names(rgb_to_hex(red, green, blue))
        self._hex_code = rgb_to_hex(red, green, blue)
        self._rgb = red, green, blue

    def darken_color(self, darkening_value=.25):
        """
        Takes a hex code and returns a hex code for a darker shade of the original hex code.
        Takes "darkening_value" as an optional input. Darkening value is a float between 0 and 1.
        """
        print("darkening color")
        h, s, v = unlist(self.hsv)
        v = v * (1 - darkening_value)
        self.hsv = format_hsv(h, s, v)

    def lighten_color(self, lightening_value=.25):
        """
        Takes a hex code and returns a hex code for a lighter shade of the original hex code.
        Takes "lightening_value" as an optional input. Lightening value is a float between 0 and 1.
        """
        print("lightening color")
        h, s, v = unlist(self.hsv)
        s = s * (1 - lightening_value)
        v = min((v * (1+lightening_value)) or (255*(lightening_value/1)), 255)
        self.hsv = format_hsv(h, s, v)

    def brighten_color(self, brightening_value=.25):
        """
        Takes a hex code and returns a hex code for a brighter shade of the original hex code.
        Takes "brightening_value" as an optional input. Brightening value is a float between 0 and 1.
        """
        print("brightening color")
        h, s, v = unlist(self.hsv)
        s = min((s + ((1 - s) * brightening_value)), 1)
        v = min((v * (1 + brightening_value), 255))
        self.hsv = format_hsv(h, s, v)

    def show_color(self, *args, **kwargs):
        if type(self.hex_code) == list:
            show_named_color(self)
        else:
            show_coded_color(self)


