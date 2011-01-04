from numpy import cos, sin, array, zeros
from contracts import contracts

@contracts(theta='number', returns='rotation_matrix')
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

@contracts(v='array[3]', returns='array[3x3],skew_symmetric')
def hat_map(v):
    h = zeros((3, 3))
    h[0, 1] = -v[2]
    h[0, 2] = v[1]
    h[1, 2] = -v[0]
    h = h - h.transpose();
    return h

@contracts(H='array[3x3],skew_symmetric', returns='array[3]')
def map_hat(H):
    v = zeros(3)
    v[2] = -H[0, 1]
    v[1] = H[0, 2]
    v[0] = -H[1, 2]
    return v
