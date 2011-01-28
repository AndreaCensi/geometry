from geometry import (random_directions, random_rotation, np,
                      best_orthogonal_transform, assert_allclose,
                      closest_orthogonal_matrix)

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
