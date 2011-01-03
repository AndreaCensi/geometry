import numpy as np 

from snp_geometry import axis_angle_from_rotation, \
    rotation_from_axis_angle, random_direction, geodesic_distance_on_S2

from .utils import rotations_sequence, axis_angle_sequence, \
    GeoTestCase

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
            dist = geodesic_distance_on_S2(s, s2)
            # Note: this is == only if axis is orthogonal to s
            assert dist <= angle

    # TODO: add test with orthogonal rotations
