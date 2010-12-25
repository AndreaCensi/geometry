import unittest

from snp_geometry import random_rotation, random_quaternion, random_direction

N = 100
    
class GeometryTests(unittest.TestCase):
    
    def test_random_quaternions(self):
        for i in range(N):
            q = random_quaternion()
        
    def test_random_rotations(self):
        for i in range(N):
            R = random_rotation()
    
    def test_random_directions(self):
        for i in range(N):
            q = random_direction()
        
