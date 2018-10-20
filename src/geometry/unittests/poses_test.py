# coding=utf-8
from geometry import (translation_angle_from_SE2, SE2_from_translation_angle,
    se2_from_linear_angular, linear_angular_from_se2, SE2_from_se2,
    se2_from_SE2,
    rot2d_from_angle, angle_from_rot2d, SE2, SE2_from_se2_slow,
    se2_from_SE2_slow,
    assert_allclose)
import numpy as np
from geometry.poses import SE3_from_SE2, se2_from_se3
from geometry.manifolds import SE3

from .utils import GeoTestCase


class PosesTest(GeoTestCase):

    def test_conversions_SE2(self):

        def sequence():
            for i in range(4):  #@UnusedVariable
                t = np.random.rand(2)
                theta = np.random.rand()
                yield t, theta

        self.check_conversion(sequence(),
                              SE2_from_translation_angle,
                              translation_angle_from_SE2)

    def test_conversions_se2(self):

        def sequence():
            for i in range(4):  #@UnusedVariable
                t = np.random.rand(2)
                theta = np.random.rand()
                yield t, theta

        self.check_conversion(sequence(),
                              se2_from_linear_angular,
                              linear_angular_from_se2)

    def test_conversions_rot2d(self):

        def sequence():
            for i in range(5):  #@UnusedVariable
                yield np.random.uniform(-np.pi, np.pi)

        self.check_conversion(sequence(),
                              rot2d_from_angle,
                              angle_from_rot2d)

    def test_conversions_se2_SE2(self):

        self.check_conversion(SE2.interesting_points(),
                              se2_from_SE2,
                              SE2_from_se2)


def comparison_test():
    ''' Compares between SE2_from_se2_slow and SE2_from_se2. '''
    for pose in SE2.interesting_points():
        se2 = se2_from_SE2(pose)
        SE2a = SE2_from_se2_slow(se2)
        SE2b = SE2_from_se2(se2)
        #printm('pose', pose, 'se2', se2)
        #printm('SE2a', SE2a, 'SE2b', SE2b)
        SE2.assert_close(SE2a, pose)
        #print('SE2a = pose Their distance is %f' % d)
        SE2.assert_close(SE2b, pose)
        #print('SE2b = pose Their distance is %f' % d)
        assert_allclose(SE2a, SE2b, atol=1e-8, err_msg='SE2a != SE2b')
        assert_allclose(SE2a, pose, atol=1e-8, err_msg='SE2a != pose')
        assert_allclose(SE2b, pose, atol=1e-8, err_msg='SE2b != pose')

def test_se3_se2():
    for pose in SE2.interesting_points():
        pose3 = SE3_from_SE2(pose)
        vel3 = SE3.algebra_from_group(pose3)
        vel2 = se2_from_se3(vel3)
        pose2= SE2.group_from_algebra(vel2)
        assert_allclose(pose2, pose, atol=1e-8)
    
def comparison_test_2():
    ''' Compares between se2_from_SE2 and se2_from_SE2_slow. '''
    for pose in SE2.interesting_points():
        se2a = se2_from_SE2(pose)
        se2b = se2_from_SE2_slow(pose)
        #printm('pose', pose, 'se2a', se2a, 'se2b', se2b)
        assert_allclose(se2a, se2b, atol=1e-8)


# Known pairs of pose, algebra
known_pairs = [
    (SE2_from_translation_angle([0, 0], np.pi),
     np.array([[0, +np.pi, 0],  # Note:  should be - if normalize_pi is changed
               [-np.pi, 0, 0],
               [0, 0, 0]])),
    (np.array([[-1, 0, 0],
               [0, -1, 0],
               [0, 0, 1]]),
     np.array([[0, np.pi, 0],
               [-np.pi, 0, 0],
               [0, 0, 0]])),
    (SE2_from_translation_angle([0, 0], 0),
     np.zeros((3, 3))),
]


def check_pi_test():
    for g, w in known_pairs:
        w2 = se2_from_SE2(g)
        # printm('g', g, 'w', w, 'w2', w2)
        assert_allclose(w, w2, atol=1e-8)
        g2 = SE2_from_se2(w2)
        assert_allclose(g, g2, atol=1e-8)

