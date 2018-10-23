# coding=utf-8
from geometry.poses import SE3_from_SE2
from geometry.poses_embedding import SE2_from_SO2, SO2_project_from_SE2, \
    SE3_from_SO3, SO3_project_from_SE3, se2_from_so2, so2_project_from_se2, \
    se3_from_so3, so3_project_from_se3, se2_project_from_se3, se3_from_se2, \
    SE2_project_from_SE3, R2_project_from_SE2, SE2_from_R2, R3_project_from_SE3, \
    SE3_from_R3
from geometry.rotations import SO2_from_angle, angle_from_SO2
from geometry.rotations_embedding import SO2_project_from_SO3, SO3_from_SO2, \
    so2_project_from_so3, so3_from_so2
from geometry.spheres import normalize_pi
from geometry.spheres_embedding import S1_project_from_S2, S2_from_S1, \
    S1_project_from_R2, S2_project_from_R3
import numpy as np

from .differentiable_manifold import DifferentiableManifold
from .euclidean import R1, R2, R3
from .special_euclidean_algebra import se3, se2
from .special_euclidean_group import SE2, SE3
from .special_orthogonal_algebra import so2, so3
from .special_orthogonal_group import SO2, SO3
from .sphere import S1, S2
from .torus import T1, T2, T3
from .translation_algebra import tran3, tran2, tran1
from .translation_group import Tran2, Tran3


def embedding(small, big, embed_in, project_from, desc=None):
    DifferentiableManifold.embedding(small, big, embed_in, project_from,
                                     itype='user', desc=desc)


def isomorphism(A, B, a_to_b, b_to_a, desc=None):
    DifferentiableManifold.isomorphism(A, B, a_to_b, b_to_a,
                                       itype='user', desc=desc)


def identity(x):
    return x


def tran1_project_from_tran2(b):
    return np.array([[0, b[0, -1]],
                    [0, 0]])


def tran2_from_tran1(b):
    return np.array([[0, 0, b[0, -1]],
                      [0, 0, 0],
                      [0, 0, 0]])


def tran2_project_from_se2(b):
    return np.array([[0, 0, b[0, -1]],
                     [0, 0, b[1, -1]],
                     [0, 0, 0]])


def tran3_project_from_se3(b):
    return np.array([[0, 0, 0, b[0, -1]],
                     [0, 0, 0, b[1, -1]],
                     [0, 0, 0, b[2, -1]],
                     [0, 0, 0, 0]])


embedding(R1, R2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embedding(R2, R3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

embedding(SO2, SO3, SO3_from_SO2, SO2_project_from_SO3)
embedding(so2, so3, so3_from_so2, so2_project_from_so3)

embedding(SO2, SE2, SE2_from_SO2, SO2_project_from_SE2)
embedding(SO3, SE3, SE3_from_SO3, SO3_project_from_SE3)

embedding(so3, se3, se3_from_so3, so3_project_from_se3)
embedding(so2, se2, se2_from_so2, so2_project_from_se2)

embedding(se2, se3, se3_from_se2, se2_project_from_se3)
embedding(SE2, SE3, SE3_from_SE2, SE2_project_from_SE3)

embedding(S1, S2, S2_from_S1, S1_project_from_S2)

embedding(S1, R2, identity, S1_project_from_R2)
embedding(S2, R3, identity, S2_project_from_R3)

embedding(R2, SE2, SE2_from_R2, R2_project_from_SE2)
embedding(R3, SE3, SE3_from_R3, R3_project_from_SE3)


def T1_from_S1(a):
    return np.array([np.cos(float(a)), np.sin(float(a))])


def S1_from_T1(b):
    return normalize_pi(np.array([np.arctan2(b[1], b[0])]))


def SO2_from_T1(x):
    return SO2_from_angle(x[0])


def T1_from_SO2(y):
    return np.array([angle_from_SO2(y)])


isomorphism(T1, S1, T1_from_S1, S1_from_T1)
isomorphism(T1, SO2, SO2_from_T1, T1_from_SO2)

embedding(T1, T2, lambda a: np.array([a[0], 0]),
              lambda b: np.array([b[0]]))
embedding(T2, T3, lambda a: np.array([a[0], a[1], 0]),
              lambda b: b[0:2])

# TODO: more tori?
embedding(T1, R1, identity, lambda x: T1.normalize(x))
embedding(T2, R2, identity, lambda x: T2.normalize(x))
embedding(T3, R3, identity, lambda x: T3.normalize(x))

embedding(tran1, tran2, tran2_from_tran1, tran1_project_from_tran2)

embedding(tran2, tran3, lambda b: np.array([[0, 0, 0, b[0, -1]],
                                            [0, 0, 0, b[1, -1]],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0]]),
                    lambda b: np.array([[0, 0, b[0, -1]],
                                         [0, 0, b[1, -1]],
                                         [0, 0, 0]]))

embedding(tran2, se2, identity, tran2_project_from_se2)

embedding(tran3, se3, identity, tran3_project_from_se3)

embedding(Tran2, SE2, identity,
                 lambda b: np.array([[1, 0, b[0, 2]],
                                     [0, 1, b[1, 2]],
                                     [0, 0, 1]]))

embedding(Tran3, SE3, identity,
                    lambda b: np.array([[1, 0, 0, b[0, -1]],
                                        [0, 1, 0, b[1, -1]],
                                        [0, 0, 1, b[2, -1]],
                                        [0, 0, 0, 1]]))

