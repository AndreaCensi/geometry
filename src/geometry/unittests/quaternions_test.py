# coding=utf-8
from geometry import quaternion_from_rotation, \
    rotation_from_quaternion, axis_angle_from_quaternion, \
    quaternion_from_axis_angle, rotation_from_axis_angle, \
    rotation_from_axis_angle2, axis_angle_from_rotation, \
    assert_allclose

from .utils import GeoTestCase, rotations_sequence, \
    quaternions_sequence, axis_angle_sequence


class TestQuaternions(GeoTestCase):

    def test_rotation_conversion1(self):
        return self.check_conversion(rotations_sequence(),
                              quaternion_from_rotation,
                              rotation_from_quaternion)

    def test_rotation_conversion2(self):
        return self.check_conversion(quaternions_sequence(),
                              rotation_from_quaternion,
                              quaternion_from_rotation)

    def test_conversions(self):
        return self.check_conversion(quaternions_sequence(),
                              axis_angle_from_quaternion,
                              quaternion_from_axis_angle)

    def test_conversions2(self):
        return self.check_conversion(axis_angle_sequence(),
                              quaternion_from_axis_angle,
                              axis_angle_from_quaternion)

    def test_rotation_from_axis_angle2(self):
        for axis, angle in axis_angle_sequence():
            R1 = rotation_from_axis_angle(axis, angle)
            R2 = rotation_from_axis_angle2(axis, angle)

            if False:
                s1, a1 = axis_angle_from_rotation(R1)
                s2, a2 = axis_angle_from_rotation(R2)
                print('Origi: %s around %s' % (angle, axis))
                print('First: %s around %s' % (a1, s1))
                print('Secnd: %s around %s' % (a2, s2))

            assert_allclose(R1, R2)
