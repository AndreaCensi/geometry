# coding=utf-8
from contracts import check, contract

import numpy as np


# TODO: write tests
@contract(X='array[KxN],K>=2,K<N', Y='array[KxN]',
          returns='array[KxK],orthogonal')
def best_orthogonal_transform(X, Y):
    ''' Finds the best orthogonal transform R  between X and Y,
        such that R X ~= Y. '''
    YX = np.dot(Y, X.T)
    check('array[KxK]', YX)
    U, _, V = np.linalg.svd(YX)
    best = np.dot(U, V)
    return best


@contract(M='array[NxN]', returns='array[NxN],orthogonal')
def closest_orthogonal_matrix(M):
    ''' Finds the closest orthogonal matrix to M. '''
    U, _, V = np.linalg.svd(M)
    R = np.dot(U, V)
    return R


# TODO: write tests
@contract(X='array[KxN],K>=2,K<N', Y='array[KxN]',
          returns='tuple( (array[KxK],orthogonal), array[Kx1])')
def best_similarity_transform(X, Y):
    ''' Finds the best transform (R,t)  between X and Y,
        such that R X + t ~= Y. '''
    K = X.shape[0]
    Xm = X.mean(axis=1).reshape(K, 1)
    Ym = Y.mean(axis=1).reshape(K, 1)
    X = X - Xm
    Y = Y - Ym
#    assert_allclose(X.mean(axis=1), 0, atol=1e-8)
#    assert_allclose(Y.mean(axis=1), 0, atol=1e-8)
    YX = np.dot(Y, X.T)
    check('array[KxK]', YX)
    U, _, V = np.linalg.svd(YX)
    R = np.dot(U, V)
    t = Ym - np.dot(R, Xm)
    return R, t

