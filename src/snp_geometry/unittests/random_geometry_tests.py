import unittest

import numpy as np

from snp_geometry import random_rotation, random_quaternion, random_direction
from contracts import check, fail
from snp_geometry.random_geometry import geodesic_distance_on_S2, \
    axis_angle_to_rotation_matrix, random_directions, \
    rotation_matrix_from_axis_angle, rotation_from_axis_angle, \
    rotation_from_axis_angle2, axis_angle_from_rotation, \
    axis_angle_from_quaternion, quaternion_from_axis_angle
from snp_geometry.utils import assert_allclose
from contracts.main import contracts


N = 20
    
class GeometryTests(unittest.TestCase):
    
    def test_random_quaternions(self):
        for i in range(N): #@UnusedVariable
            random_quaternion()
        
    def test_random_rotations(self):
        for i in range(N): #@UnusedVariable
            random_rotation()
    
    def test_random_direction(self):
        for i in range(N): #@UnusedVariable
            random_direction()
        
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
        
    def test_random_directions(self):
        N = 20
        x = random_directions(N)
        assert x.shape == (3, N)
        
    def test_distances(self):
        for i in range(N): #@UnusedVariable
            s = random_direction()
            dist = geodesic_distance_on_S2 
            assert_allclose(dist(s, s), 0)
            assert_allclose(dist(s, -s), np.pi)

class TestQuaternions(unittest.TestCase):
    
    def test_conversions(self):
        for i in range(N): #@UnusedVariable
            q = random_quaternion() 
            axis, angle = axis_angle_from_quaternion(q)
            q2 = quaternion_from_axis_angle(axis, angle)
            assert_allclose(q, q2)

    def test_conversions2(self):
        for i in range(N): #@UnusedVariable
            axis, angle = random_axis_angle()
            q = quaternion_from_axis_angle(axis, angle)
            axis2, angle2 = axis_angle_from_quaternion(q)
            assert_allclose(axis, axis2)
            assert_allclose(angle, angle2)
            
            
@contracts(returns='tuple(direction, (float,<3.15))')
def random_axis_angle():
    max_angle = np.pi * 0.9 
    angle = np.random.uniform() * max_angle
    axis = random_direction()
    return axis, angle

class AxisAngleTests(unittest.TestCase):

    def test_distances_rotations(self):
        for i in range(N): #@UnusedVariable
            s = random_direction()
            axis, angle = random_axis_angle()
            R = rotation_from_axis_angle(axis, angle)
            s2 = np.dot(R, s)
            dist = geodesic_distance_on_S2(s, s2)
            # Note: this is == only if axis is orthogonal to s
            assert dist <= angle
        
    def test_axis_angle(self):
        for i in range(N): #@UnusedVariable
            max_angle = np.pi * 0.9 
            angle = np.random.uniform() * max_angle
            axis = random_direction()
            R1 = rotation_from_axis_angle(axis, angle)
            R2 = rotation_from_axis_angle2(axis, angle)
            
            s1, a1 = axis_angle_from_rotation(R1)
            s2, a2 = axis_angle_from_rotation(R2)
            print('Origi: %s around %s' % (angle, axis))
            print('First: %s around %s' % (a1, s1))
            print('Secnd: %s around %s' % (a2, s2))
            
            assert_allclose(R1, R2)

    def test_axis_angle2(self):
        for i in range(N): #@UnusedVariable
            max_angle = np.pi * 0.9 
            angle = np.random.uniform() * max_angle
            axis = random_direction()
            R = rotation_from_axis_angle(axis, angle)
            check('rotation_matrix', R)
            axis2, angle2 = axis_angle_from_rotation(R)
            assert_allclose(angle, angle2)
            assert_allclose(axis, axis2)

    def test_axis_angle3(self):
        for i in range(N): #@UnusedVariable
            R = random_rotation() 
            axis, angle = axis_angle_from_rotation(R)
            R2 = rotation_from_axis_angle(axis, angle)
            assert_allclose(R, R2)
