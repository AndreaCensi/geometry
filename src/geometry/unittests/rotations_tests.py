import numpy as np 

from geometry import (axis_angle_from_rotation,
    rotation_from_axis_angle, random_direction, hat_map,
    geodesic_distance_on_sphere, assert_allclose) 

from .utils import rotations_sequence, axis_angle_sequence, \
    GeoTestCase, directions_sequence

class RotationsTest(GeoTestCase):

    def test_conversions1(self):
        return self.check_conversion(rotations_sequence(),
                              axis_angle_from_rotation,
                              rotation_from_axis_angle)

    def test_conversions2(self):
        return self.check_conversion(axis_angle_sequence(),
                              rotation_from_axis_angle,
                              axis_angle_from_rotation)

    def test_distances_rotations(self):
        for axis, angle in axis_angle_sequence():
            s = random_direction()
            R = rotation_from_axis_angle(axis, angle)
            s2 = np.dot(R, s)
            dist = geodesic_distance_on_sphere(s, s2)
            # Note: this is == only if axis is orthogonal to s
            assert dist <= angle

    # TODO: add test with orthogonal rotations

def hat_map_test():
    for s in directions_sequence():
        for v in directions_sequence():
            x1 = np.cross(s, v)
            x2 = +np.dot(hat_map(s), v)
            x3 = -np.dot(hat_map(v), s)
            assert_allclose(x1, x2)
            assert_allclose(x1, x3)
            
            
        
    
