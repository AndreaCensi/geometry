from . import contract, dot, svd, check

# TODO: write tests
@contract(X='array[KxN],K>=2,K<N', Y='array[KxN]', returns='array[KxK],orthogonal')
def best_orthogonal_transform(X, Y):
    ''' Finds the best orthogonal transform R  between X and Y,
        such that R X ~= Y. '''
    YX = dot(Y, X.T)
    check('array[KxK]', YX)
    U, S, V = svd(YX) #@UnusedVariable
    best = dot(U, V)
    return best


@contract(M='array[NxN]', returns='array[NxN],orthogonal')
def closest_orthogonal_matrix(M):
    ''' Finds the closest orthogonal matrix to M. '''
    U, S, V = svd(M) #@UnusedVariable
    R = dot(U, V)
    return R
