import unittest
 
from numpy import array
import numpy
from snp_geometry.utils import map_hat, hat_map

class UtilsTests(unittest.TestCase):
    def hat_test(self):
        for v in [[1,2,3]]:
            v=array(v)
            H = hat_map(v)
            v2 = map_hat(H)
            numpy.testing.assert_almost_equal(v, v2, 7)
