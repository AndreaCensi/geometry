 
from snp_geometry.utils import map_hat, hat_map
from snp_geometry.unittests.utils import GeoTestCase, directions_sequence

class UtilsTests(GeoTestCase):
    def hat_test(self):
        self.check_conversion(directions_sequence(), hat_map, map_hat)
