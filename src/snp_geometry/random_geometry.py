
import numpy as np

from numpy import cos, sin, sqrt
from numpy.random import uniform

from contracts import contracts 


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
    return quaternion_to_rotation_matrix(q)


@contracts(x='unit_quaternion', returns='rotation_matrix')
def quaternion_to_rotation_matrix(x):
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

# TODO add finite
@contracts(axis='direction', angle='float', returns='unit_quaternion')
def axis_angle_to_quaternion(axis, angle):
    return np.array([
            axis[0] * sin(angle / 2),
            axis[1] * sin(angle / 2),
            axis[2] * sin(angle / 2),
            cos(angle / 2)
        ])

@contracts(axis='direction', angle='float', returns='rotation_matrix')
def axis_angle_to_rotation_matrix(axis, angle):
    q = axis_angle_to_quaternion(axis, angle)
    return quaternion_to_rotation_matrix(q)
    
    

@contracts(returns='array[3x3], orthogonal')
def random_orthogonal_transform():
    # TODO: to write
    pass

@contracts(how_many='int,>0,N', returns='array[3xN]')
def random_directions(how_many):
    ''' Returns a list of random directions. '''
    return np.array([random_direction().T for i in range(how_many)]) #@UnusedVariable


