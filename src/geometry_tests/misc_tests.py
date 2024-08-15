from geometry import hat_map, map_hat
from .utils import directions_sequence, GeoTestCase


class UtilsTests(GeoTestCase):
    def hat_test(self):
        self.check_conversion(directions_sequence(), hat_map, map_hat)
