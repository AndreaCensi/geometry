from geometry import hat_map
from geometry import map_hat

from .utils import GeoTestCase
from .utils import directions_sequence


class UtilsTests(GeoTestCase):
    def hat_test(self):
        self.check_conversion(directions_sequence(), hat_map, map_hat)
