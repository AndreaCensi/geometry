# coding=utf-8
import unittest

from nose.plugins.attrib import attr

from contracts import check, fail
from contracts.enabling import all_disabled
from geometry import (random_rotation, random_quaternion, random_direction,
    random_directions_bounded, any_distant_direction, any_orthogonal_direction,
    distribution_radius, geodesic_distance_on_sphere, assert_orthogonal,
    rotation_from_axis_angle, default_axis, default_axis_orthogonal,
    random_orthogonal_direction, random_directions, assert_allclose)
import numpy as np

from .utils import directions_sequence

N = 20


class GeometryTests(unittest.TestCase):

    def is_contracts_active(self):
        return not all_disabled()

    # TODO: add statistics test
    def test_random_quaternions(self):
        for i in range(N):  #@UnusedVariable
            random_quaternion()

    def test_random_rotations(self):
        for i in range(N):  #@UnusedVariable
            random_rotation()

    def test_random_direction(self):
        for i in range(N):  #@UnusedVariable
            random_direction()

    def test_checks(self):
        if not self.is_contracts_active():
            return
        R = np.zeros((10, 10))
        fail('rotation_matrix', R)
        R = random_rotation()
        R[0, 2] += R[0, 1]
        fail('rotation_matrix', R)

        R = random_rotation()
        R *= 2
        fail('rotation_matrix', R)

    def test_unit_length(self):
        if not self.is_contracts_active():
            return
        check('unit_length', np.array([1]))
        check('unit_length', np.array([0, 1]))
        fail('unit_length', np.array([0, 2]))

    def test_random_directions(self):
        N = 20
        x = random_directions(N)
        assert x.shape == (3, N)

    def test_distances(self):
        for i in range(N):  #@UnusedVariable
            s = random_direction()
            dist = geodesic_distance_on_sphere
            assert_allclose(dist(s, s), 0)
            assert_allclose(dist(s, -s), np.pi)


@attr('density')
def random_directions_bounded_test_1():
    # TODO: write actual test
    r = np.pi / 2
    N = 180
    random_directions_bounded(ndim=2, radius=r, num_points=N, center=None)
    random_directions_bounded(ndim=3, radius=r, num_points=N, center=None)
    random_directions_bounded(ndim=2, radius=r, num_points=N,
                              center=random_direction(2))
    random_directions_bounded(ndim=3, radius=r, num_points=N,
                              center=random_direction(3))


def check_reasonable_radius(r, r2, N):  #@UnusedVariable
    bounds = [0.8, 1.2]  # TODO: make it depend on N
    if not (r * bounds[0] <= r2 <= r * bounds[1]):
        msg = 'Constructed distribution with radius %f, got %f.' % (r, r2)
        assert False, msg


def random_directions_bounded_check(ndim, radius, N):
    S = random_directions_bounded(ndim=ndim, radius=radius, num_points=N)
    r2 = distribution_radius(S)
    check_reasonable_radius(radius, r2, N)


@attr('density')
def random_directions_bounded_test():
    radius = [np.pi, np.pi / 2, np.pi / 6]
    N = 300
    for ndim in [2, 3]:
        for r in radius:
            yield random_directions_bounded_check, ndim, r, N


def distribution_radius_check(center, radius, N):
    angles = (np.random.rand(N) - 0.5) * 2 * radius
    angles += center
    S = np.vstack((np.cos(angles), np.sin(angles)))
    r2 = distribution_radius(S)
    check_reasonable_radius(radius, r2, N)


def distribution_radius_test():
    radius = [np.pi, np.pi / 2, np.pi / 6]
    N = 300
    for r in radius:
        for i in range(5):  #@UnusedVariable
            center = np.random.rand() * 2 * np.pi
            yield distribution_radius_check, center, r, N


def any_distant_direction_test():
    for s in directions_sequence():
        z = any_distant_direction(s)
        d = geodesic_distance_on_sphere(z, s)
        assert d > np.pi / 6


def any_orthogonal_direction_test():
    for s in directions_sequence():
        for i in range(5):  #@UnusedVariable
            z = any_orthogonal_direction(s)
            assert_orthogonal(z, s)


def random_orthogonal_direction_test():
    for s in directions_sequence():
        for i in range(5):  #@UnusedVariable
            z = random_orthogonal_direction(s)
            assert_orthogonal(z, s)


def default_axis_orthogonal_test():
    z1 = default_axis()
    z2 = default_axis_orthogonal()
    assert_orthogonal(z1, z2)


def sorted_directions_test():
    # TODO
    pass


# TODO: write tests for ndim=2
def assert_orthogonal_test():
    for s in directions_sequence():
        axis = any_orthogonal_direction(s)
        angle = np.pi / 2
        R = rotation_from_axis_angle(axis, angle)
        s2 = np.dot(R, s)
        assert_orthogonal(s, s2)

