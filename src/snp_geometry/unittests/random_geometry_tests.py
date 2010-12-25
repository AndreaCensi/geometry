import numpy
import unittest

from snp_geometry import random_rotation, random_quaternion

class GeometryTests(unittest.TestCase):
    
    def test_random_rotations(self):
        for i in range(50):
            q = random_quaternion()
        
        for i in range(50):
            R = random_rotation()
    
