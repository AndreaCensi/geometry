# coding=utf-8
from contracts import contract
from geometry.poses import SE2_from_rotation_translation, \
    rotation_translation_from_SE2, extract_pieces, SE3_from_rotation_translation, \
    rotation_translation_from_SE3, combine_pieces
from geometry.rotations import map_hat_2d, hat_map
from geometry.rotations_embedding import so3_from_so2, SO2_project_from_SO3, \
    so2_project_from_so3
import numpy as np


@contract(returns='SE2', a='SO2')
def SE2_from_SO2(a):
    return SE2_from_rotation_translation(a, np.array([0, 0]))


@contract(returns='SO2', b='SE2')
def SO2_project_from_SE2(b):
    return rotation_translation_from_SE2(b)[0]


@contract(returns='se2', a='so2')
def se2_from_so2(a):
    omega = map_hat_2d(a)
    return hat_map(np.array([0, 0, omega]))


@contract(returns='so2', b='se2')
def so2_project_from_se2(b):
    return extract_pieces(b)[0]


@contract(returns='SE3', a='SO3')
def SE3_from_SO3(a):
    return SE3_from_rotation_translation(a, np.array([0, 0, 0]))


@contract(returns='SO3', b='SE3')
def SO3_project_from_SE3(b):
    return rotation_translation_from_SE3(b)[0]


@contract(returns='se3', a='so3')
def se3_from_so3(a):
    return combine_pieces(a, np.array([0, 0, 0]), np.array([0, 0, 0]), 0)


@contract(returns='so3', b='se3')
def so3_project_from_se3(b):
    return extract_pieces(b)[0]


@contract(returns='SE2', a='R2')
def SE2_from_R2(a):
    return SE2_from_rotation_translation(np.eye(2), a)


@contract(returns='SE3', a='R3')
def SE3_from_R3(a):
    return SE3_from_rotation_translation(np.eye(3), a)


@contract(returns='R2', b='SE2')
def R2_project_from_SE2(b):
    return rotation_translation_from_SE2(b)[1]


@contract(returns='R3', b='SE3')
def R3_project_from_SE3(b):
    return rotation_translation_from_SE3(b)[1]


@contract(returns='se3', a='se2')
def se3_from_se2(a):
    W, v, zero, one = extract_pieces(a)  # @UnusedVariable
    W = so3_from_so2(W)
    v = np.array([v[0], v[1], 0])
    return combine_pieces(W, v, v * 0, 0)


@contract(returns='SE2', b='SE3')
def SE2_project_from_SE3(b):
    R, t, zero, one = extract_pieces(b)  # @UnusedVariable
    R = SO2_project_from_SO3(R)
    t = t[0:2]
    return combine_pieces(R, t, t * 0, 1)


@contract(returns='se2', b='se3')
def se2_project_from_se3(b):
    W, v, zero, one = extract_pieces(b)  # @UnusedVariable
    W = so2_project_from_so3(W)
    v = v[0:2]
    return combine_pieces(W, v, v * 0, 0)

