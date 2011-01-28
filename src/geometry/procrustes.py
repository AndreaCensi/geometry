from .common_imports import *

# TODO: write tests
@contract(X='array[KxN],K>=2,K<N', Y='array[KxN]', returns='array[KxK],orthogonal')
def best_orthogonal_transform(X, Y):
    ''' Finds the best orthogonal transform R  between X and Y,
        such that R X ~= Y. '''
    YX = np.dot(Y, X.T)
    check('array[KxK]', YX)
    U, S, V = np.linalg.svd(YX) #@UnusedVariable
    best = np.dot(U, V)
    return best


@contract(M='array[NxN]', returns='array[NxN],orthogonal')
def closest_orthogonal_matrix(M):
    ''' Finds the closest orthogonal matrix to M. '''
    U, S, V = np.linalg.svd(M) #@UnusedVariable
    R = np.dot(U, V)
    return R
