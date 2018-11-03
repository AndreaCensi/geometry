# coding=utf-8
'''
    Contains all about rotation matrices, quaternions, and various conversions.

    conventions: q=( a + bi + cj + dk), with a>0
'''
import itertools

import numpy as np
from contracts import contract, new_contract, raise_wrapped, raise_desc

from .basic_utils import safe_arccos, normalize_length
from .spheres import default_axis

new_contract('unit_quaternion', 'array[4], unit_length')
new_contract('axis_angle', 'tuple(direction, float)')
# Canonically, we return a positive angle.
new_contract('axis_angle_canonical', 'tuple(direction, (float,>=0, <=pi))')


@contract(x='array[NxN],N>0')
def check_SO(x):
    ''' Checks that the given value is a rotation matrix of arbitrary size. '''
    try:
        check_orthogonal(x)
    except ValueError as e:
        msg = 'It is not orthogonal.'
        raise_wrapped(ValueError, e, msg, x=x, compact=True)
    determinant = np.linalg.det(x * 1.0)  # XXX: voodoo
    # lapack_lite.LapackError:
    # Parameter a has non-native byte order in lapack_lite.dgetrf
    if not np.allclose(determinant, 1.0):
        msg = 'The determinant is %s not 1.' % determinant
        raise_desc(ValueError, msg, x=x)


@contract(x='array[NxN],N>0')
def check_orthogonal(x):
    ''' Check that the argument is an orthogonal matrix. '''
    a = np.dot(x, x.T)
    b = np.dot(x.T, x)
    try:
        check_diagonal(a)
        check_diagonal(b)
    except ValueError as e:
        msg = 'It looks like it is not orthonal'
        raise_wrapped(ValueError, e, msg, a=a, b=b)


def check_diagonal(m, rtol=10E-10, atol=10E-7):
    shape = m.shape
    for i, j in itertools.product(range(shape[0]), range(shape[1])):
        if i != j:
            if not np.allclose(m[i, j], 0, rtol=rtol, atol=atol):
                msg = 'The element %s, %s is %s not equal to zero.' % (i, j, m[i, j])
                raise ValueError(msg)


@contract(x='array[NxN]')
def check_skew_symmetric(x):
    ''' Check that the argument is a skew-symmetric matrix. '''
    n = x.shape[0]
    ok = (np.zeros((n, n)) == x).all()
    if not ok:
        diag = x.diagonal()
        if not (diag == 0).all():
            raise ValueError('Expected skew symmetric, but diagonal is not '
                             'exactly zero: %s.' % diag)
        for i, j in itertools.product(range(n), range(n)):
            if i < j:
                continue
            if x[i, j] != -x[j, i]:
                raise ValueError('Expected skew symmetric, but ' +
                                 'a[%d][%d] = %f, a[%d][%d] = %f' % \
                                 (i, j, x[i, j], j, i, x[j, i]))


new_contract('orthogonal', check_orthogonal)
new_contract('SO', check_SO)
new_contract('skew_symmetric', check_skew_symmetric)

new_contract('SO2', 'array[2x2],SO')
new_contract('SO3', 'array[3x3],SO')

new_contract('so', 'skew_symmetric')
new_contract('so2', 'array[2x2],skew_symmetric')
new_contract('so3', 'array[3x3],skew_symmetric')

# deprecated
new_contract('rotation_matrix', 'SO3')


@contract(theta='number', returns='SO3')
def rotz(theta):
    ''' Returns a 3x3 rotation matrix corresponding
        to rotation around the *z* axis. '''
    C = np.cos(theta)
    S = np.sin(theta)
    return np.array([
        [C, -S, 0],
        [S, +C, 0],
        [0, 0, 1]])


@contract(w='array[3]', returns='SO3')
def SO3_from_R3(w):  # untested
    from geometry.manifolds import so3, SO3
    R = SO3.group_from_algebra(so3.algebra_from_vector(w))
    return R


@contract(theta='number', returns='SO3')
def rotx(theta):
    ''' Returns a 3x3 rotation matrix corresponding
        to rotation around the *x* axis. '''
    w = np.array([theta, 0, 0])
    return SO3_from_R3(w)


@contract(theta='number', returns='SO3')
def roty(theta):
    ''' Returns a 3x3 rotation matrix corresponding
        to rotation around the *x* axis. '''
    w = np.array([0, theta, 0])
    return SO3_from_R3(w)


@contract(theta='number', returns='SO2')
def SO2_from_angle(theta):
    ''' Returns a 2x2 rotation matrix. '''
    C = np.cos(theta)
    S = np.sin(theta)
    return np.array([
        [+C, -S],
        [+S, +C]])


@contract(# M='O2',
          returns='tuple(float, float)')
def angle_scale_from_O2(M):
    p = np.dot(M, [1, 0])
    angle = np.arctan2(p[1], p[0])
    scale = np.linalg.norm(p)
    if angle == np.pi:
        angle = -np.pi
    return angle, scale


@contract(R='SO2', returns='float')
def angle_from_SO2(R):
    angle = np.arctan2(R[1, 0], R[0, 0])
    if angle == np.pi:
        angle = -np.pi
    return angle


@contract(omega='number', returns='so2')
def hat_map_2d(omega):
    return np.array([[0, -1], [+1, 0]]) * omega


@contract(W='so2', returns='float')
def map_hat_2d(W):
    return W[1, 0]


rot2d = SO2_from_angle  # TODO: deprecated
rot2d_from_angle = SO2_from_angle  # TODO: deprecated
angle_from_rot2d = angle_from_SO2


@contract(returns='unit_quaternion')
def random_quaternion():
    ''' Generate a random quaternion.

        Uses the algorithm used in Kuffner, ICRA'04.
    '''
    s = np.random.uniform()
    sigma1 = np.sqrt(1 - s)
    sigma2 = np.sqrt(s)
    theta1 = np.random.uniform() * 2 * np.pi
    theta2 = np.random.uniform() * 2 * np.pi

    q = np.array([np.cos(theta2) * sigma2,
                  np.sin(theta1) * sigma1,
                  np.cos(theta1) * sigma1,
                  np.sin(theta2) * sigma2])

    q *= np.sign(q[0])
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
        return rot2d(np.random.uniform(0, 2 * np.pi))
    else:
        assert False


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
    R = np.dot(R1, R2.T)
    axis1, angle1 = axis_angle_from_rotation(R)  # @UnusedVariable
    return angle1


@contract(v='array[3]', returns='array[3x3],skew_symmetric')
def hat_map(v):
    ''' Maps a vector to a 3x3 skew symmetric matrix. '''
    h = np.zeros((3, 3))
    h[0, 1] = -v[2]
    h[0, 2] = v[1]
    h[1, 2] = -v[0]
    h = h - h.transpose()
    return h


@contract(H='array[3x3],skew_symmetric', returns='array[3]')
def map_hat(H):
    ''' The inverse of :py:func:`hat_map`. '''
    v = np.zeros(3)
    v[2] = -H[0, 1]
    v[1] = H[0, 2]
    v[0] = -H[1, 2]
    return v


@contract(x='unit_quaternion', returns='rotation_matrix')
def rotation_from_quaternion(x):
    '''
        Converts a quaternion to a rotation matrix.

    '''
    # Documented in <http://en.wikipedia.org/w/index.php?title=
    # Quaternions_and_spatial_rotation&oldid=402924915>
    a, b, c, d = x

    r1 = [a ** 2 + b ** 2 - c ** 2 - d ** 2,
          2 * b * c - 2 * a * d,
          2 * b * d + 2 * a * c]
    r2 = [2 * b * c + 2 * a * d,
          a ** 2 - b ** 2 + c ** 2 - d ** 2,
          2 * c * d - 2 * a * b]
    r3 = [2 * b * d - 2 * a * c,
          2 * c * d + 2 * a * b,
          a ** 2 - b ** 2 - c ** 2 + d ** 2]

    return np.array([r1, r2, r3])


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
    if r == 0:  # TODO: add tolerance
        return quaternion_from_axis_angle(default_axis(), 0.0)
    else:
        q0 = (R[w, v] - R[v, w]) / (2 * r)
        qu = (r / 2)
        qv = (R[u, v] + R[v, u]) / (2 * r)
        qw = (R[w, u] + R[u, w]) / (2 * r)

        Q = np.zeros(4)
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
    Q = np.array([
        np.cos(angle / 2),
        axis[0] * np.sin(angle / 2),
        axis[1] * np.sin(angle / 2),
        axis[2] * np.sin(angle / 2)
    ])
    Q *= np.sign(Q[0])
    return Q


@contract(q='unit_quaternion', returns='axis_angle_canonical')
def axis_angle_from_quaternion(q):
    '''
        This is the inverse of :py:func:`quaternion_from_axis_angle`.
    '''
    angle = 2 * safe_arccos(q[0])
    if angle == 0:  # XXX: use tolerance
        axis = default_axis()
    else:
        axis = q[1:] / np.sin(angle / 2)
    axis = axis / np.linalg.norm(axis)
    if angle > np.pi:
        angle -= 2 * np.pi
    elif angle < -np.pi:
        angle += 2 * np.pi

    return axis, angle


@contract(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle(axis, angle):
    '''
        Computes the rotation matrix from the *(axis,angle)* representation
        using Rodriguez's formula.
    '''
    w = axis
    w_hat = hat_map(w)
    w_hat2 = np.dot(w_hat, w_hat)
    R = np.eye(3) + w_hat * np.sin(angle) + w_hat2 * (1 - np.cos(angle))
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
        v = np.array([R[2, 1] - R[1, 2],
                      R[0, 2] - R[2, 0],
                      R[1, 0] - R[0, 1]])

        computer_with_infinite_precision = False
        if computer_with_infinite_precision:
            axis = (1 / (2 * np.sin(angle))) * v
        else:
            # OK, the formula above gives (theoretically) the correct answer
            # but it is imprecise if angle is small (dividing by a very small
            # quantity). This is way better...
            axis = (v * np.sign(angle)) / np.linalg.norm(v)

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
def rotation_from_axes_spec(x_axis, vector_on_xy_plane):  # TODO: docs
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
