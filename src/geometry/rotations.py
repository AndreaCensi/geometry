''' Contains all about rotation matrices, quaternions, and various conversions.

     conventions: q=( a + bi + cj + dk), with a>0
'''
import itertools
from . import (assert_allclose, new_contract, contract, dot, zeros, eye,
               safe_arccos, arctan2, np,
               pi, sin, cos, array, sign, uniform, argmax, sqrt, check,
               default_axis, norm, normalize_length)



new_contract('unit_quaternion', 'array[4], unit_length')
new_contract('axis_angle', 'tuple(direction, float)') 
# Canonically, we return a positive angle.
new_contract('axis_angle_canonical', 'tuple(direction, (float,>=0, <=pi))')


@new_contract
def SO(x):
    ''' Checks that the given value is a rotation matrix of arbitrary size. '''
    check('orthogonal', x)
    determinant = np.linalg.det(x * 1.0) # XXX: voodoo
    # lapack_lite.LapackError: Parameter a has non-native byte order in lapack_lite.dgetrf
    assert_allclose(determinant, 1.0) 

@new_contract
@contract(x='array[NxN],N>0')
def orthogonal(x):
    N = x.shape[0]
    I = eye(N) 
    rtol = 10E-10 # XXX:
    atol = 10E-7  # XXX:
    assert_allclose(I, dot(x, x.T), rtol=rtol, atol=atol)
    assert_allclose(I, dot(x.T, x), rtol=rtol, atol=atol)

@new_contract
@contract(x='array[NxN]')
def skew_symmetric(x):
    n = x.shape[0]
    ok = (zeros((n, n)) == x).all()
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
                
                

new_contract('SO2', 'array[2x2],SO')
new_contract('SO3', 'array[3x3],SO')

new_contract('so', 'skew_symmetric')
new_contract('so2', 'array[2x2],skew_symmetric')
new_contract('so3', 'array[3x3],skew_symmetric')

# deprecated
new_contract('rotation_matrix', 'SO3')

@contract(theta='number', returns='SO3')
def rotz(theta):
    ''' Returns a 3x3 rotation matrix corresponding to rotation around the *z* axis. '''
    return array([ 
            [ cos(theta), -sin(theta), 0],
            [ sin(theta), cos(theta), 0],
            [0, 0, 1]]) 

@contract(theta='number', returns='SO2')
def SO2_from_angle(theta):
    ''' Returns a 2x2 rotation matrix. '''
    return array([ 
            [ cos(theta), -sin(theta)],
            [ sin(theta), cos(theta)]]) 

@contract(R='SO2', returns='float')
def angle_from_SO2(R):
    angle = arctan2(R[1, 0], R[0, 0])
    if angle == np.pi:
        angle = -np.pi
    return angle

def hat_map_2d(omega):
    return np.array([[0, -1], [+1, 0]]) * omega

def map_hat_2d(W):
    return W[1, 0]



rot2d = SO2_from_angle # TODO: deprecated 
rot2d_from_angle = SO2_from_angle# TODO: deprecated 
angle_from_rot2d = angle_from_SO2


@contract(returns='unit_quaternion')
def random_quaternion():
    ''' Generate a random quaternion.
        
        Uses the algorithm used in Kuffner, ICRA'04.
    '''
    s = uniform()
    sigma1 = sqrt(1 - s)
    sigma2 = sqrt(s)
    theta1 = uniform() * 2 * pi
    theta2 = uniform() * 2 * pi

    q = array([cos(theta2) * sigma2,
                  sin(theta1) * sigma1,
                  cos(theta1) * sigma1,
                  sin(theta2) * sigma2 ])
    
    q *= sign(q[0])
    return q

@contract(returns='array[2x2]|rotation_matrix', ndim='2|3')
def random_rotation(ndim=3):
    ''' Generate a random rotation matrix. 
        
        This is a wrapper around :py:func:`random_quaternion`.
    '''
    if ndim == 3:
        q = random_quaternion()
        return rotation_from_quaternion(q)
    elif ndim == 2:
        return rot2d(uniform(0, 2 * pi))
    else: assert False

@contract(returns='array[3x3], orthogonal')
def random_orthogonal_transform():
    # TODO: to write
    assert False, 'Not implemented'


@contract(R1='rotation_matrix', R2='rotation_matrix', returns='float,>=0,<=pi')
def geodesic_distance_for_rotations(R1, R2):
    ''' 
        Returns the geodesic distance between two rotation matrices.
        
        It is computed as the angle of the rotation :math:`R_1^{*} R_2^{-1}``.
    
    '''
    R = dot(R1, R2.T)
    axis1, angle1 = axis_angle_from_rotation(R) #@UnusedVariable
    return angle1 


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
    largest = argmax(R.diagonal())
    permutations = {0: [0, 1, 2],
                    1: [1, 2, 0],
                    2: [2, 0, 1]}
    u, v, w = permutations[largest]
    rr = 1 + R[u, u] - R[v, v] - R[w, w]
    assert rr >= 0
    r = sqrt(rr)
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
    Q *= sign(Q[0])
    return Q

@contract(q='unit_quaternion', returns='axis_angle_canonical')
def axis_angle_from_quaternion(q):
    ''' 
        This is the inverse of :py:func:`quaternion_from_axis_angle`.
    '''
    angle = 2 * safe_arccos(q[0])
    if angle == 0: # XXX: use tolerance
        axis = default_axis()
    else:
        axis = q[1:] / sin(angle / 2)
    axis = axis / norm(axis)
    if angle > pi:
        angle -= 2 * pi
    elif angle < -pi:
        angle += 2 * pi
        
    return axis, angle
         

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
        goes through the quaternion representation instead of using Rodrigues'
        formula.
    '''
    q = quaternion_from_axis_angle(axis, angle)
    return rotation_from_quaternion(q)

@contract(x_axis='direction', vector_on_xy_plane='direction',
          returns='rotation_matrix')
def rotation_from_axes_spec(x_axis, vector_on_xy_plane): # TODO: docs
    """ 
        Creates a rotation matrix from the axes. 
        ``x_axis`` is the new direction of the (1,0,0) vector
        after this rotation. ``vector_on_xy_plane`` is a vector
        that must end up in the (x,y) plane after the rotation. 
        
        That is, it holds that: ::
        
            R = rotation_from_axes_spec(x, v)
            dot(R,x) == [1,0,0]
            dot(R,v) == [?,?,0]
     
        TODO: add exception if vectors are too close.
    """
    z_axis = normalize_length(np.cross(x_axis, vector_on_xy_plane))
    y_axis = normalize_length(np.cross(z_axis, x_axis))
    R = np.vstack((x_axis, y_axis, z_axis))
    return R.copy('C')
