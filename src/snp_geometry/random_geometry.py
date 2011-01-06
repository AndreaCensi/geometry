from .common_imports import *
from .rotations import (rotation_from_quaternion,
                         default_axis_orthogonal, normalize_pi,
                        rotation_from_axis_angle, default_axis)
from .distances import geodesic_distance_on_sphere, normalize_length, distances_from
from .utils import rot2d, sphere_area, spherical_cap_with_area
from snp_geometry.utils import spherical_cap_area


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

@contracts(returns='array[2x2]|rotation_matrix', ndim='2|3')
def random_rotation(ndim=3):
    ''' Generate a random rotation matrix. 
        Wraps :py:func:`random_quaternion`.
    '''
    if ndim == 3:
        q = random_quaternion()
        return rotation_from_quaternion(q)
    elif ndim == 2:
        return rot2d(uniform(0, 2 * pi))
    else: assert False

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
        theta = np.sign(uniform() - 0.5) * pi / 2
        return dot(rot2d(theta), s)
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
        a certain radius from center. The points will be distributed
        uniformly in that area of the sphere.
        If center is not passed, it will be a random direction. 
    '''
    if center is None:
        center = random_direction(ndim)
        
    directions = np.empty((ndim, num_points))
    for i in range(num_points):
        # move the center of a random amount 
        if ndim == 3:
            # sample axis orthogonal to the center
            axis = random_orthogonal_direction(center)
            z = uniform(0, 1) * spherical_cap_area(radius)
            distance = spherical_cap_with_area(z)
            R = rotation_from_axis_angle(axis, distance)
        elif ndim == 2:
            angle = uniform(-radius, radius)
            R = rot2d(angle)
        else: assert False
        direction = np.dot(R, center)
        directions[:, i] = direction
        
    return sorted_directions(directions)

@contracts(S='array[KxN],(K=2|K=3),directions', returns='array[KxN], directions')
def sorted_directions(S, num_around=15):
    ''' 
        In 2D, sorts the directions. 
    
        In 3D, makes a pleasant elicoidal arrangement.
    '''
    if S.shape[0] == 2:
        # XXX check nonzero
        center = np.arctan2(S[1, :].sum(), S[0, :].sum()) 
        angles = np.arctan2(S[1, :], S[0, :])
        diffs = normalize_pi(angles - center)
        sorted = np.sort(diffs)
        final = center + sorted
        return np.vstack((np.cos(final), np.sin(final)))
    else:
        # find center of distribution
        center = normalize_length(S.sum(axis=1))
        # compute the distances from the center
        distance = distances_from(S, center)
        # compute the phase from an arbitrary axis
        axis = any_orthogonal_direction(center)
        phase = distances_from(S, axis)
        # normalize distances and phase in [0,1]
        phase = (normalize_pi(phase) + pi) / (2 * pi)
        distance /= distance.max()
        
        score = distance * num_around + phase
        
        order = np.argsort(score)
        
        ordered = S[:, order]
        return ordered
    
