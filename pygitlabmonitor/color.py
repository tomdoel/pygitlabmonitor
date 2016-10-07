import math


class Color(object):
    def __init__(self, r, g, b):
        self._color = (r, g, b)

    def get_contrast_colour(self):
        if self.get_luminance() > 0.179:
            return Color(0, 0, 0)
        else:
            return Color(255, 255, 255)

    def get_luminance(self):
        r = self.convert(self._color[0])
        g = self.convert(self._color[1])
        b = self.convert(self._color[2])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def convert(value):
        value /= 255.0
        if value <= 0.03928:
            value /= 12.92
        else:
            value = math.pow(((value + 0.055) / 1.055), 2.4)
        return value

    def get_str(self):
        return "#%02X%02X%02X" % self._color
