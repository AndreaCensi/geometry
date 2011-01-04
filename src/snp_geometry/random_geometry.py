from .common_imports import * 
from .rotations import (rotation_from_quaternion, hat_map,
                        rotation_from_axis_angle, default_axis)
from .distances import geodesic_distance_on_sphere
from .utils import rot2d
from .rotations import default_axis_orthogonal

@contracts(ndim='(2|3),K', returns='array[K],unit_length')
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
        return np.array([cos(theta), sin(theta)])
        
    else: assert False


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

@contracts(returns='array[3x3], orthogonal')
def random_orthogonal_transform():
    # TODO: to write
    pass

@contracts(how_many='int,>0,N', ndim="2|3", returns='array[3xN]')
def random_directions(how_many, ndim=3):
    ''' Returns a list of random directions. '''
    return np.vstack([random_direction(ndim) 
                      for i in range(how_many)]).T #@UnusedVariable

@contracts(s='direction', returns='direction')
def any_distant_direction(s):
    ''' Returns a direction distant from both s and -s. '''
    z = default_axis()
    d = geodesic_distance_on_sphere(s, z)
    limit = 1.0 / 6.0 * pi
    if min(d, pi - d) < limit:
        z = default_axis_orthogonal()
    return z

@contracts(s='direction', returns='direction')
def any_orthogonal_direction(s):
    ''' Returns any axis orthogonal to s. '''
    # choose a vector far away
    z = any_distant_direction(s)
    # z ^ s is orthogonal to s
    x = np.cross(z, s)
    v = x / norm(x)
    return v

@contracts(s='array[K],unit_length', returns='array[K],unit_length')
def random_orthogonal_direction(s):
    ''' Returns a random axis orthogonal to s. '''
    if s.size == 2:
        if uniform() < 0.5:
            return dot(rot2d(pi / 2), s)
        else: 
            return dot(rot2d(-pi / 2), s)
    elif s.size == 3:
        # get any axis orthogonal to s
        z = any_orthogonal_direction(s)
        # rotate this axis around s by a random amount
        angle = uniform(0, 2 * pi)
        R = rotation_from_axis_angle(s, angle)
        z2 = np.dot(R, z)
        return z2
    else: assert False

@contracts(ndim='(2|3),K',
           radius='number,>0,<=3.15',
           num_points='int,>0',
           center='None|(array[K],unit_length)',
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
        angle = uniform(-radius, radius)
        if ndim == 3:
            # sample axis orthogonal to the center
            axis = random_orthogonal_direction(center)
            R = rotation_from_axis_angle(axis, angle)
        elif ndim == 2:
            R = rot2d(angle)
        else: assert False
        direction = np.dot(R, center)
        directions[:, i] = direction
        
    return directions

