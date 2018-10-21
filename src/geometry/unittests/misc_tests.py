# coding=utf-8
from geometry import map_hat, hat_map

from .utils import GeoTestCase, directions_sequence


class UtilsTests(GeoTestCase):

    def hat_test(self):
        self.check_conversion(directions_sequence(), hat_map, map_hat)
