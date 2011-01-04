import numpy as np

from contracts import new_contract, contracts
import itertools

def assert_allclose(actual, desired, rtol=1e-7, atol=0,
                    err_msg='', verbose=True):
    ''' Backporting assert_allclose from 1.5 to 1.4 '''
    from numpy.testing.utils import assert_array_compare
    def compare(x, y):
        return np.allclose(x, y, rtol=rtol, atol=atol)
    actual, desired = np.asanyarray(actual), np.asanyarray(desired)
    header = 'Not equal to tolerance rtol=%g, atol=%g' % (rtol, atol)
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
                         verbose=verbose, header=header)

@new_contract
@contracts(x='array[N],N>0')
def unit_length(x):
    assert_allclose(1, np.linalg.norm(x), rtol=1e-5)

new_contract('direction', 'array[3], unit_length')
new_contract('unit_quaternion', 'array[4], unit_length')


@new_contract
@contracts(x='array')
def finite(x):
    # TODO: make into standard thing
    return np.isfinite(x).all()



@new_contract
@contracts(x='array[NxN],N>0')
def orthogonal(x):
    N = x.shape[0]
    I = np.eye(N) 
    rtol = 10E-10
    atol = 10E-7
    assert_allclose(I, np.dot(x, x.T), rtol=rtol, atol=atol)
    assert_allclose(I, np.dot(x.T, x), rtol=rtol, atol=atol)

@new_contract
@contracts(x='array[3x3], orthogonal')
def rotation_matrix(x):
    det = np.linalg.det(x)
    assert_allclose(det, 1) 

@new_contract
@contracts(x='array[NxN]')
def skew_symmetric(x):
    n = x.shape[0]
    ok = (np.zeros((n, n)) == x).all()
    if not ok:
        diag = x.diagonal()
        if not (diag == 0).all():
            raise ValueError('Expected skew symmetric, but diagonal is not '
                             'exactly zero: %s.' % diag)
        for i, j in itertools.product(range(n), range(n)):
            if i < j: continue
            if x[i, j] != -x[j, i]:
                raise ValueError('Expected skew symmetric, but ' + 
                                 'a[%d][%d] = %f, a[%d][%d] = %f' % \
                                 (i, j, x[i, j], j, i, x[j, i]))

@new_contract
@contracts(X='array[KxN],K>0,N>0')
def directions(X):
    ''' Checks that every column has unit length. '''
    K = X.shape[1]
    for i in range(K):
        v = X[:, i]
        assert_allclose(1, np.linalg.norm(v) , rtol=1e-5)
