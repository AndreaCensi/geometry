# coding=utf-8
from contracts import contract
from geometry.rotations import angle_from_rot2d, rotation_from_axis_angle, rot2d, \
    map_hat_2d, hat_map
import numpy as np


@contract(returns='SO3', a='SO2')
def SO3_from_SO2(a):
    theta = angle_from_rot2d(a)
    return rotation_from_axis_angle(np.array([0, 0, 1]), theta)


@contract(returns='SO2', b='SO3')
def SO2_project_from_SO3(b):
    direction = np.array([1, 0, 0])
    vector = np.dot(b, direction)
    n = np.linalg.norm(vector)
    atol = 1e-8  # XXX: make common
    if n < atol:
        return rot2d(0)
    else:
        theta = np.arctan2(vector[1], vector[0])
        return rot2d(theta)


@contract(returns='so3', a='so2')
def so3_from_so2(a):
    omega = map_hat_2d(a)
    return hat_map(np.array([0, 0, omega]))


@contract(returns='so2', b='so3')
def so2_project_from_so3(b):
    return b[0:2, 0:2]
