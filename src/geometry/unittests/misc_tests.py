from .utils import GeoTestCase, directions_sequence
from geometry import map_hat, hat_map


class UtilsTests(GeoTestCase):
    def hat_test(self):
        self.check_conversion(directions_sequence(), hat_map, map_hat)
