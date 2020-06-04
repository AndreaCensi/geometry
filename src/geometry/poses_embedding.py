# coding=utf-8
import numpy as np

from .poses import (
    combine_pieces,
    extract_pieces,
    rotation_translation_from_SE2,
    rotation_translation_from_SE3,
    SE2_from_rotation_translation,
    SE3_from_rotation_translation,
)
from .rotations import hat_map, map_hat_2d
from .rotations_embedding import SO2_project_from_SO3, so2_project_from_so3, so3_from_so2
from .types import SE3value, se3value, SO3value, so3value, T2value, T3value

__all__ = [
    "SE2_from_SO2",
    "SO2_project_from_SE2",
    "se2_from_so2",
    "so2_project_from_se2",
    "SE3_from_SO3",
    "SO3_project_from_SE3",
    "se3_from_so3",
    "so3_project_from_se3",
    "SE2_from_R2",
    "SE3_from_R3",
    "R2_project_from_SE2",
    "R3_project_from_SE3",
    "se2_project_from_se3",
    "se3_from_se2",
]

from .types import SE2value, se2value, SO2value, so2value


def SE2_from_SO2(a: SO2value) -> SE2value:
    return SE2_from_rotation_translation(a, np.array([0, 0]))


def SO2_project_from_SE2(b: SE2value) -> SO2value:
    r, _ = rotation_translation_from_SE2(b)
    return r


def se2_from_so2(a: so2value) -> se2value:
    omega = map_hat_2d(a)
    return hat_map(np.array([0, 0, omega]))


def so2_project_from_se2(b: so2value) -> SO2value:
    return extract_pieces(b)[0]


def SE3_from_SO3(a: SO3value) -> SE3value:
    return SE3_from_rotation_translation(a, np.array([0, 0, 0]))


def SO3_project_from_SE3(b: SE3value) -> SO3value:
    return rotation_translation_from_SE3(b)[0]


def se3_from_so3(a: so3value) -> se3value:
    return combine_pieces(a, np.array([0, 0, 0]), np.array([0, 0, 0]), 0)


def so3_project_from_se3(b: se3value) -> so3value:
    return extract_pieces(b)[0]


def SE2_from_R2(a: T2value) -> SE2value:
    return SE2_from_rotation_translation(np.eye(2), a)


def SE3_from_R3(a: T3value) -> SE3value:
    return SE3_from_rotation_translation(np.eye(3), a)


def R2_project_from_SE2(b: SE2value) -> T2value:
    return rotation_translation_from_SE2(b)[1]


def R3_project_from_SE3(b: SE3value) -> T3value:
    return rotation_translation_from_SE3(b)[1]


def se3_from_se2(a: se2value) -> se3value:
    W, v, zero, one = extract_pieces(a)
    W = so3_from_so2(W)
    v = np.array([v[0], v[1], 0])
    return combine_pieces(W, v, v * 0, 0)


def SE2_project_from_SE3(b: SE3value) -> SE2value:
    R, t, zero, one = extract_pieces(b)
    R = SO2_project_from_SO3(R)
    t = t[0:2]
    return combine_pieces(R, t, t * 0, 1)


def se2_project_from_se3(b: se3value) -> se2value:
    W, v, zero, one = extract_pieces(b)
    W = so2_project_from_so3(W)
    v = v[0:2]
    return combine_pieces(W, v, v * 0, 0)
