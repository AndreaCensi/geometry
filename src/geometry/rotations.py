''' Contains all about rotation matrices, quaternions, and various conversions.

     conventions: q=( a + bi + cj + dk), with a>0
'''
from .common_imports import *

def safe_arccos(x):
    ''' 
        Returns the arcosine of x, clipped between -1 and 1.
        
        Use this when you know x is a cosine, but it might be
        slightly over 1 or below -1 due to numerical errors.
    '''
    return np.arccos(np.clip(x, -1.0, 1.0))

@contract(v='array[3]', returns='array[3x3],skew_symmetric')
def hat_map(v):
    ''' Maps a vector to a 3x3 skew symmetric matrix. '''
    h = zeros((3, 3))
    h[0, 1] = -v[2]
    h[0, 2] = v[1]
    h[1, 2] = -v[0]
    h = h - h.transpose()
    return h

@contract(H='array[3x3],skew_symmetric', returns='array[3]')
def map_hat(H):
    ''' The inverse of :py:func:`hat_map`. '''
    v = zeros(3)
    v[2] = -H[0, 1]
    v[1] = H[0, 2]
    v[0] = -H[1, 2]
    return v


def normalize_pi(x):
    ''' Normalizes the entries in *x* in the interval :math:`[-pi,pi)`. '''
    return np.arctan2(np.sin(x), np.cos(x))


@contract(x='unit_quaternion', returns='rotation_matrix')
def rotation_from_quaternion(x):
    '''
        Converts a quaternion to a rotation matrix.
        
        Documented in <http://en.wikipedia.org/w/index.php?title=Quaternions_and_spatial_rotation&oldid=402924915>
    '''
    a, b, c, d = x
        
    r1 = [a ** 2 + b ** 2 - c ** 2 - d ** 2,
          2 * b * c - 2 * a * d,
          2 * b * d + 2 * a * c ]
    r2 = [2 * b * c + 2 * a * d,
          a ** 2 - b ** 2 + c ** 2 - d ** 2,
          2 * c * d - 2 * a * b]
    r3 = [2 * b * d - 2 * a * c,
          2 * c * d + 2 * a * b,
          a ** 2 - b ** 2 - c ** 2 + d ** 2]
    
    return array([r1, r2, r3])

@contract(R='rotation_matrix', returns='unit_quaternion')
def quaternion_from_rotation(R):
    ''' 
        Converts a rotation matrix to a quaternion.
    
        This is the robust method mentioned on wikipedia:
    
        <http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>
        
        TODO: add the more robust method with 4x4 matrix and eigenvector
    '''
    largest = np.argmax(R.diagonal())
    permutations = {0: [0, 1, 2],
                    1: [1, 2, 0],
                    2: [2, 0, 1]}
    u, v, w = permutations[largest]
    rr = 1 + R[u, u] - R[v, v] - R[w, w]
    assert rr >= 0
    r = np.sqrt(rr)
    if r == 0: # TODO: add tolerance
        return quaternion_from_axis_angle(default_axis(), 0.0)
    else:
        q0 = (R[w, v] - R[v, w]) / (2 * r)
        qu = (r / 2)
        qv = (R[u, v] + R[v, u]) / (2 * r)
        qw = (R[w, u] + R[u, w]) / (2 * r)
        
        Q = zeros(4)
        Q[0] = q0
        Q[u + 1] = qu
        Q[v + 1] = qv
        Q[w + 1] = qw
        if Q[0] < 0:
            Q = -Q
        return Q


@contract(axis='direction', angle='float', returns='unit_quaternion')
def quaternion_from_axis_angle(axis, angle):
    ''' 
        Computes a quaternion corresponding to the rotation of *angle* radians
        around the given *axis*.
        
        This is the inverse of :py:func:`axis_angle_from_quaternion`.
    '''
    Q = array([
            cos(angle / 2),
            axis[0] * sin(angle / 2),
            axis[1] * sin(angle / 2),
            axis[2] * sin(angle / 2)
        ])
    Q *= np.sign(Q[0])
    return Q

@contract(q='unit_quaternion', returns='axis_angle_canonical')
def axis_angle_from_quaternion(q):
    ''' 
        This is the inverse of :py:func:`quaternion_from_axis_angle`.
    '''
    angle = 2 * safe_arccos(q[0])
    if angle == 0: # XXX: use tolerance
        axis = default_axis
    else:
        axis = q[1:] / sin(angle / 2)
    if angle > pi:
        angle -= 2 * pi
    elif angle < -pi:
        angle += 2 * pi
        
    return axis, angle
         
@contract(returns='direction')
def default_axis(): 
    ''' 
        Returns the axis to use when any will do. 
        
        For example, the identity is represented by
        a rotation of 0 degrees around *any* axis. If an *(axis,angle)*
        representation is requested, the axis will be given by
        *default_axis()*. 
    '''
    return  array([0.0, 0.0, 1.0])

@contract(returns='direction')
def default_axis_orthogonal():
    ''' 
        Returns an axis orthogonal to the one returned 
        by :py:func:`default_axis`. 
        
        Use this when you need a couple of arbitrary orthogonal axes.
    '''  
    return  array([0.0, 1.0, 0.0])

@contract(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle(axis, angle):
    ''' 
        Computes the rotation matrix from the *(axis,angle)* representation
        using Rodriguez's formula. 
    '''
    w = axis
    w_hat = hat_map(w)
    w_hat2 = dot(w_hat, w_hat)
    R = eye(3) + w_hat * sin(angle) + w_hat2 * (1 - cos(angle))
    return R

@contract(R='rotation_matrix', returns='axis_angle_canonical')
def axis_angle_from_rotation(R):
    ''' 
        Returns the *(axis,angle)* representation of a given rotation.
        
        There are a couple of symmetries:
    
        * By convention, the angle returned is nonnegative.
         
        * If the angle is 0, any axis will do. 
          In that case, :py:func:`default_axis` will be returned. 
          
    '''
    angle = safe_arccos((R.trace() - 1) / 2)
    
    if angle == 0:
        return default_axis(), 0.0
    else:
        v = array([R[2, 1] - R[1, 2],
                   R[0, 2] - R[2, 0],
                   R[1, 0] - R[0, 1]])
        axis = (1 / (2 * sin(angle))) * v
        return axis, angle
    
@contract(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle2(axis, angle):
    ''' 
        Get the rotation from the *(axis,angle)* representation.
        
        This is an alternative to :py:func:`rotation_from_axis_angle` which
        goes through the quaternion representation.
    '''
    q = quaternion_from_axis_angle(axis, angle)
    return rotation_from_quaternion(q)
     
