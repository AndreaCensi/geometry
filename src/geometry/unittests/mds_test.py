# coding=utf-8
import itertools

from geometry import (euclidean_distances, assert_allclose, double_center, mds,
    mds_randomized, place, eigh)
import numpy as np


def euclidean_distances_test():
    n = 5
    P = np.random.rand(3, n)
    D = euclidean_distances(P)
    assert D.shape == (n, n)
    for i, j in itertools.product(range(n), range(n)):
        d = np.linalg.norm(P[:, i] - P[:, j])
        assert_allclose(d, D[i, j])


def rank_test():
    ''' Check that the double-centered matrix has small rank. '''
    for n in range(5, 50, 5):
        for k in range(1, 5):
            P = np.random.rand(k, n)
            D = euclidean_distances(P)
            B = double_center(D * D)
            w, v = eigh(B)  #@UnusedVariable
            w = w[::-1]  # descending
            # normalize
            wn = w / w[0]
            small = np.abs(wn[k])
            assert_allclose(0, small, atol=1e-7)
#            print('k = %d n = %d  small = %s' % (k, n, small))


def evaluate_error(P1, P2):
    D1 = euclidean_distances(P1)
    D2 = euclidean_distances(P2)
    return np.abs(D1 - D2).mean()


def mds_test():
    for n in [10, 100]:
        for k in [3, 4, 5]:
            P = np.random.rand(k, n)
            D = euclidean_distances(P)
            P2 = mds(D, ndim=k)
            error = evaluate_error(P, P2)
            assert_allclose(0, error, atol=1e-7)
#            print('k = %d n = %d  mean_error = %s' % (k, n, error))


def mds_fast_test():
    for n in [10, 100]:
        for k in [2, 3]:
            P = np.random.rand(k, n)
            D = euclidean_distances(P)

            for algo in [mds, mds_randomized]:
#                t0 = time.clock()
                P2 = algo(D, ndim=k)
#                t1 = time.clock()
                #t_mds = t1 - t0
                #            D2 = euclidean_distances(P2)
                error = evaluate_error(P, P2)
                assert_allclose(0, error, atol=1e-7)
                #print('k = %d n = %d  %-20s  %7d ms   mean_error = %s' %
                #      (k, n, algo.__name__, t_mds * 1000, error))


def place_test():
    for n in [4, 10]:
        for k in [3]:
            S = np.random.rand(k, n)
            p = np.random.rand(k)
            ref = lambda x: np.linalg.norm(p - x)
            distances = np.array([ref(S[:, i]) for i in range(n)])
            p2 = place(S, distances)
            assert_allclose(p, p2)

