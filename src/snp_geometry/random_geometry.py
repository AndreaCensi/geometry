import numpy as np

from numpy import cos, sin, sqrt, pi
from numpy.random import uniform

from contracts import contracts 
from snp_geometry.utils import hat_map
from snp_geometry.geometry_contracts import assert_allclose


# conventions: q=( a + bi + cj + dk), with a>0

@contracts(ndim='2|3', returns='direction')
def random_direction(ndim=3):
    ''' Generates a random direction in S^2. '''
    if ndim == 3:
        z = uniform(-1, +1)
        t = uniform(0, 2 * pi)
        r = sqrt(1 - z ** 2)
        x = r * cos(t)
        y = r * sin(t)
        return np.array([x, y, z])
    elif ndim == 2:
        theta = uniform(0, 2 * pi)
        return np.array([np.cos(theta), np.sin(theta)])
        
    else: assert False


#def so3_geodesic(r, r0):
#    # r, r0: cgtypes.mat3
#    r_mat = mat(r).T
#    r0_mat = mat(r0).T
#    return abs(myacos((trace(r0_mat.T * r_mat)-1)/2))


@contracts(s='direction', v='direction', returns='float,>=0,<=3.1416')
def geodesic_distance_on_S2(s, v):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s == v).all(): return 0.0
    dot_product = np.clip((s * v).sum(), -1, 1) # safe to clip if directions
    return np.arccos(dot_product) # safe to arccos() if clipped

@contracts(s='array[K],unit_length', v='array[K],unit_length', returns='float,>=0,<=3.1416')
def geodesic_distance_on_sphere(s, v):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s == v).all(): return 0.0
    dot_product = np.clip((s * v).sum(), -1, 1) # safe to clip if directions
    return np.arccos(dot_product) # safe to arccos() if clipped


@contracts(returns='unit_quaternion')
def random_quaternion():
    ''' Generate a random quaternion.
        Uses the algorithm used in Kuffner, ICRA'04.
    '''
    s = uniform()
    sigma1 = sqrt(1 - s)
    sigma2 = sqrt(s)
    theta1 = uniform() * 2 * pi
    theta2 = uniform() * 2 * pi

    q = np.array([cos(theta2) * sigma2,
                  sin(theta1) * sigma1,
                  cos(theta1) * sigma1,
                  sin(theta2) * sigma2 ])
    
    q *= np.sign(q[0])
    return q

@contracts(returns='rotation_matrix')
def random_rotation():
    ''' Generate a random rotation matrix. 
        Wraps :py:func:`random_quaternion`.
    '''
    q = random_quaternion()
    return rotation_from_quaternion(q)


@contracts(x='unit_quaternion', returns='rotation_matrix')
def rotation_from_quaternion(x):
    '''
        From: <http://en.wikipedia.org/w/index.php?title=Quaternions_and_spatial_rotation&oldid=402924915>
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
    
    return np.array([r1, r2, r3])

@contracts(R='rotation_matrix', returns='unit_quaternion')
def quaternion_from_rotation(R):
    ''' Robust method mentioned on wikipedia:
        http://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
        
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
        
        Q = np.zeros(4)
        Q[0] = q0
        Q[u + 1] = qu
        Q[v + 1] = qv
        Q[w + 1] = qw
        if Q[0] < 0:
            Q = -Q
        return Q

# TODO: remove
quaternion_to_rotation_matrix = rotation_from_quaternion

# TODO add finite
@contracts(axis='direction', angle='float', returns='unit_quaternion')
def quaternion_from_axis_angle(axis, angle):
    Q = np.array([
            cos(angle / 2),
            axis[0] * sin(angle / 2),
            axis[1] * sin(angle / 2),
            axis[2] * sin(angle / 2)
        ])
    Q *= np.sign(Q[0])
    return Q

@contracts(q='unit_quaternion', returns='tuple(direction, (float,<3.15))')
def axis_angle_from_quaternion(q):
    angle = 2 * np.arccos(q[0])
    if angle == 0: # XXX: use tolerance
        axis = default_axis
    else:
        axis = q[1:] / sin(angle / 2)
    if angle > pi:
        angle -= 2 * pi
    elif angle < -pi:
        angle += 2 * pi
        
    return axis, angle
         
@contracts(returns='direction')
def default_axis(): 
    return  np.array([0, 0, 1])

@contracts(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle(axis, angle):
    w = axis
    w_hat = hat_map(w)
    w_hat2 = np.dot(w_hat, w_hat)
    # Rodriguez' formula
    R = np.eye(3) + w_hat * np.sin(angle) + w_hat2 * (1 - np.cos(angle))
    return R

@contracts(R='rotation_matrix', returns='tuple(direction,(float,<3.15))')
def axis_angle_from_rotation(R):
    angle = np.arccos((R.trace() - 1) / 2)
    
    if angle == 0:
        return default_axis(), 0.0
    else:
        v = np.array([R[2, 1] - R[1, 2],
                      R[0, 2] - R[2, 0],
                      R[1, 0] - R[0, 1]])
        axis = (1 / (2 * np.sin(angle))) * v
        return axis, angle
    
@contracts(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle2(axis, angle):
    q = quaternion_from_axis_angle(axis, angle)
    return rotation_from_quaternion(q)
    
# old aliases to remove
rotation_matrix_from_axis_angle = rotation_from_axis_angle
axis_angle_to_rotation_matrix = rotation_matrix_from_axis_angle
    
@contracts(returns='array[3x3], orthogonal')
def random_orthogonal_transform():
    # TODO: to write
    pass

@contracts(how_many='int,>0,N', ndim="2|3", returns='array[3xN]')
def random_directions(how_many, ndim=3):
    ''' Returns a list of random directions. '''
    return np.vstack([random_direction(ndim) 
                      for i in range(how_many)]).T #@UnusedVariable

def assert_orthogonal(s, v):
    assert_allclose((v * s).sum(), 0)
    
def any_distant_direction(s):
    ''' Returns a direction distant from both s and -s. '''
    z = np.array([0, 0, 1])
    d = geodesic_distance_on_sphere(s, z)
    limit = 1.0 / 6.0 * pi
    if min(d, pi - d) < limit:
        z = np.array([1, 0, 0])
    
    d = geodesic_distance_on_sphere(s, z)
    assert min(d, pi - d) < limit
    return z
    
def any_orthogonal_direction(s):
    ''' Returns any axis orthogonal to s. '''
    # choose a vector far away
    z = any_distant_direction(s)
    # z ^ s is orthogonal to s
    ortho = np.dot(hat_map(z), s)
    assert_orthogonal(s, ortho)
    return ortho

def random_orthogonal_direction(s):
    ''' Returns a random axis orthogonal to s. '''
    # get any axis orthogonal to s
    z = any_orthogonal_direction(s)
    # rotate this axis around s by a random amount
    angle = uniform(0, 2 * pi)
    R = rotation_from_axis_angle(s, angle)
    z2 = np.dot(R, z)
    assert_orthogonal(s, z2)
    return z2


@contracts(ndim='(2|3),K',
           radius='number,>0,<=3.15',
           num_points='int,>0',
           center='None|(array[K],direction)',
           returns='array[KxN],directions')
def random_directions_bounded(ndim, radius, num_points, center=None):
    ''' Returns a random distribution of points in S^ndim within
        a certain radius from center. If center is not passed, 
        it will be random as well. 
    '''
    if center is None:
        center = random_direction(ndim)
        
    directions = np.empty((ndim, num_points))
    for i in range(num_points):
        # move the center of a random amount
        # XXX: I'm not sure this is correct, but it is good enough
        angle = uniform(0, radius)
        # any axis orthogonal to the center will do
        axis = random_orthogonal_direction(center)
        R = rotation_from_axis_angle(axis, angle)
        direction = np.dot(R, center)
        directions[:, i] = direction
        
    return directions

