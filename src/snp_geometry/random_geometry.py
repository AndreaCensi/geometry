import numpy as np

from numpy import cos, sin, sqrt
from numpy.random import uniform

from contracts import contracts 
from snp_geometry.utils import hat_map


@contracts(returns='direction')
def random_direction():
    ''' Generates a random direction in S^2. '''
    # Generate a random direction
    z = uniform(-1., 1.)
    t = uniform(0, 2 * np.pi)
    r = sqrt(1 - z ** 2)
    x = r * cos(t)
    y = r * sin(t)
    return np.array([x, y, z])


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

@contracts(returns='unit_quaternion')
def random_quaternion():
    ''' Generate a random quaternion.
        Uses the algorithm used in Kuffner, ICRA'04.
    '''
    s = uniform()
    sigma1 = sqrt(1 - s)
    sigma2 = sqrt(s)
    theta1 = uniform(0, 2 * np.pi)
    theta2 = uniform(0, 2 * np.pi)

    q = [cos(theta2) * sigma2,
         sin(theta1) * sigma1,
         cos(theta1) * sigma1,
         sin(theta2) * sigma2 ]
    
    return np.array(q)

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

quaternion_to_rotation_matrix = rotation_from_quaternion
# TODO add finite
@contracts(axis='direction', angle='float', returns='unit_quaternion')
def quaternion_from_axis_angle(axis, angle):
    return np.array([
            cos(angle / 2),
            axis[0] * sin(angle / 2),
            axis[1] * sin(angle / 2),
            axis[2] * sin(angle / 2)
        ])

@contracts(q='unit_quaternion', returns='tuple(direction, (float,<3.15))')
def axis_angle_from_quaternion(q):
    angle = 2 * np.arccos(q[0])
    if angle == 0: # XXX: use tolerance
        axis = default_axis
    else:
        axis = q[1:] / sin(angle / 2)
    if angle > np.pi:
        angle -= 2 * np.pi
    elif angle < -np.pi:
        angle += 2 * np.pi
        
    return axis, angle
         
@contracts(returns='direction')
def default_axis(): 
    return  np.array([0, 0, 1])

@contracts(axis='direction', angle='float', returns='rotation_matrix')
def rotation_from_axis_angle(axis, angle):
    w = axis
    w_hat = hat_map(w)
    w_hat2 = np.dot(w_hat, w_hat)
    R = np.eye(3) + w_hat * np.sin(angle) + w_hat2 * (1 - np.cos(angle))
    return R

@contracts(R='rotation_matrix', returns='tuple(direction,(float,<3.15))')
def axis_angle_from_rotation(R):
    angle = np.arccos((R.trace() - 1) / 2)
    
    if angle == 0:
        return default_axis(), 0
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
    

rotation_matrix_from_axis_angle = rotation_from_axis_angle
axis_angle_to_rotation_matrix = rotation_matrix_from_axis_angle
    
@contracts(returns='array[3x3], orthogonal')
def random_orthogonal_transform():
    # TODO: to write
    pass

@contracts(how_many='int,>0,N', returns='array[3xN]')
def random_directions(how_many):
    ''' Returns a list of random directions. '''
    return np.vstack([random_direction() for i in range(how_many)]).T #@UnusedVariable


