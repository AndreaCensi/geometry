import itertools
import warnings

from .common_imports import *

@contracts(s='array[K],K>=2', v='array[K]')
def assert_orthogonal(s, v):
    ''' Checks that two vectors are orthogonal. '''
    dot = (v * s).sum()
    if not np.allclose(dot, 0):
        angle = np.arccos(dot / (norm(v) * norm(s)))
        msg = ('Angle is %.2f deg between %s and %s.' 
               % (np.degrees(angle), s, v)) 
        assert_allclose(dot, 0, err_msg=msg)
    
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
    ''' Checks that the value is a 1D vector with unit length in the 2 norm.'''
    assert_allclose(1, np.linalg.norm(x), rtol=1e-5)

new_contract('direction', 'array[3], unit_length')
new_contract('unit_quaternion', 'array[4], unit_length')
new_contract('axis_angle', 'tuple(direction, (float,<3.15))') # TODO: pi

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
    ''' Checks that the given value is a rotation matrix. '''
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
        
def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    def new_func(*args, **kwargs):
        # TODO: mofify stack
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func
