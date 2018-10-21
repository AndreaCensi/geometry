# coding=utf-8
import unittest

from contracts import contract
from geometry import (random_direction, random_quaternion, random_rotation,
    assert_allclose)
import numpy as np

N = 20


def rotations_sequence():
    yield np.eye(3)
    # TODO: add special values
    for i in range(N):  # @UnusedVariable
        yield random_rotation()


def directions_sequence():
    ''' Sequence of directions in S^2. '''
    yield np.array([1.0, 0.0, 0.0])
    yield np.array([0.0, 1.0, 0.0])
    yield np.array([0.0, 0.0, 1.0])
    yield np.array([-1.0, 0.0, 0.0])
    yield np.array([0.0, -1.0, 0.0])
    yield np.array([0.0, 0.0, -1.0])
    # TODO: add special values
    for i in range(N):  # @UnusedVariable
        yield random_direction(3)


def quaternions_sequence():
    # TODO: add special values
    for i in range(N):  # @UnusedVariable
        yield random_quaternion()


def axis_angle_sequence():
    # TODO: add special
    for i in range(N):  # @UnusedVariable
        yield random_axis_angle()


@contract(returns='tuple(direction, (float,<3.15))')
def random_axis_angle():
    max_angle = np.pi * 0.9
    angle = np.random.uniform() * max_angle
    axis = random_direction()
    return axis, angle


class GeoTestCase(unittest.TestCase):

    def check_one(self, x, op1, op2):

        def call(function, param):
            if isinstance(param, tuple):
                return function(*param)
            else:
                return function(param)

        y = call(op1, x)
        x2 = call(op2, y)

        if isinstance(x, tuple):
            for a, b in zip(x, x2):
                assert_allclose(a, b)
        else:
            assert_allclose(x, x2)

    def check_conversion(self, sequence, op1, op2):
        ''' Checks that  x = op2(op1(x)) for all x in sequence.
            If intermediate results are tuples, they are passed
            as distinct parameters. '''

        for x in sequence:
            # yield self.check_one, x, op1, op2
            self.check_one(x, op1, op2)

