# coding=utf-8
from geometry import (random_directions, random_rotation, np,
                      best_orthogonal_transform, assert_allclose,
                      closest_orthogonal_matrix)
from geometry.procrustes import best_similarity_transform


def best_orthogonal_transform_test1():
    X = random_directions(20)
    R = random_rotation()
    Y = np.dot(R, X)
    R2 = best_orthogonal_transform(X, Y)
    assert_allclose(R, R2)


def best_orthogonal_transform_test2():
    N = 20
    X = random_directions(N)
    Y = random_directions(N)
    R1 = best_orthogonal_transform(X, Y)
    R2 = best_orthogonal_transform(Y, X)
    assert_allclose(R1.T, R2)


def closest_orthogonal_matrix_test1():
    R = random_rotation()
    R2 = closest_orthogonal_matrix(R)
    assert_allclose(R, R2)


def best_similarity_transform_test():
    N = 20
    for K in [3]:  # TODO: multiple dimensions
        X = np.random.randn(K, N)

        R = random_rotation()
#        R = np.eye(K)
        t = np.random.randn(K, 1)
#        print 'R: %s' % R
#        print 't: %s' % t

        Y = np.dot(R, X) + t
        R2, t2 = best_similarity_transform(X, Y)
#        print 'R2: %s' % R2
#        print 't2: %s' % t2
        Y2 = np.dot(R2, X) + t2

        assert_allclose(R, R2, atol=1e-10)
        assert_allclose(t, t2)

        assert_allclose(Y, Y2)

