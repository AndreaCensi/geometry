# coding=utf-8
from contracts import contract

import numpy as np

from .. import assert_allclose


@contract(A='array[NxK]')
def normalize_columns(A):
    A = A.copy()
    _, k = A.shape
    for j in range(k):
        A[:, j] = A[:, j] / np.linalg.norm(A[:, j])
    return A


@contract(A='array[NxK]')
def proj_from_subspace(A):
    An = normalize_columns(A)
    return np.dot(An, An.T)


def get_random_proj(n, k):
    A = np.random.randn(n, k)
    return proj_from_subspace(A)


@contract(P='array[NxN]')
def assert_projection(P):
    assert_allclose(P.T, P)
    assert_allclose(np.dot(P, P), P)


def check():
    # XXX
    n = 6
    P1 = get_random_proj(n, 1)
    P2 = get_random_proj(n, 1)

    C = np.dot(P1, P2)
    assert_projection(P1)
    assert_projection(P2)

    assert_projection(C)
