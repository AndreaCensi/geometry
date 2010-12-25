import unittest

import numpy as np

from snp_geometry import random_rotation, random_quaternion, random_direction
from contracts import check, fail


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
            s = random_direction()
        
    def test_checks(self):
        R = np.zeros((10, 10))
        fail('rotation_matrix', R)
        R = random_rotation()
        R[0, 2] += R[0, 1]
        fail('rotation_matrix', R)

        R = random_rotation()
        R *= 2
        fail('rotation_matrix', R)

    def test_unit_length(self):
        
        check('unit_length', np.array([1]))
        check('unit_length', np.array([0, 1]))
        fail('unit_length', np.array([0, 2]))
