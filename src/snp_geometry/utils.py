from numpy import cos, sin, array, zeros
from .numpy_checks import require_length, \
    require_skew_symmetric, require_array_with_shape
from contracts.main import contracts

def rotz(theta):
    ''' Returns a 3x3 rotation matrix corresponding to rotation around the z axis. '''
    return array([ 
            [ cos(theta), -sin(theta), 0],
            [ sin(theta), cos(theta), 0],
            [0, 0, 1]]) 


def rot2d(theta):
    ''' Returns a 2x2 rotation matrix. '''
    return array([ 
            [ cos(theta), -sin(theta)],
            [ sin(theta), cos(theta)]]) 

@contracts(v='array[3]', returns='array[3x3]')
def hat_map(v):
    h = zeros((3, 3))
    h[0, 1] = -v[2]
    h[0, 2] = v[1]
    h[1, 2] = -v[0]
    h = h - h.transpose();
    return h

def map_hat(H):
    
    require_array_with_shape(H, (3, 3))
    require_skew_symmetric(H)

    v = zeros(3)
    v[2] = -H[0, 1]
    v[1] = H[0, 2]
    v[0] = -H[1, 2]

    return v


def assert_allclose(actual, desired, rtol=1e-7, atol=0,
                    err_msg='', verbose=True):
    ''' Backporting assert_allclose from 1.5 to 1.4 '''
    from numpy.testing.utils import assert_array_compare
    import numpy as np
    def compare(x, y):
        return np.allclose(x, y, rtol=rtol, atol=atol)
    actual, desired = np.asanyarray(actual), np.asanyarray(desired)
    header = 'Not equal to tolerance rtol=%g, atol=%g' % (rtol, atol)
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
                         verbose=verbose, header=header)


