from . import (cos, sin, pi, sqrt, arccos, clip, safe_arccos, normalize_length,
               contract, new_contract, assert_allclose, np, dot, norm,
               array, uniform, vstack, argmin)

@new_contract
@contract(x='array[N],N>0')
def unit_length(x):
    ''' Checks that the value is a 1D vector with unit length in the 2 norm.'''
    assert_allclose(1, norm(x), rtol=1e-5) # XXX:

new_contract('direction', 'array[3], unit_length')

new_contract('S1', 'array[2],unit_length')
new_contract('S2', 'array[3],unit_length')

@new_contract
@contract(X='array[KxN],K>0,N>0')
def directions(X):
    ''' Checks that every column has unit length. '''
    norm = (X * X).sum(axis=0)
    assert_allclose(1, norm , rtol=1e-5) # XXX:
        


@contract(s='array[K],K>=2', v='array[K]')
def assert_orthogonal(s, v):
    ''' Checks that two vectors are orthogonal. '''
    dot = (v * s).sum()
    if not np.allclose(dot, 0):
        angle = np.arccos(dot / (norm(v) * norm(s)))
        msg = ('Angle is %.2f deg between %s and %s.' 
               % (np.degrees(angle), s, v)) 
        assert_allclose(dot, 0, err_msg=msg)
    
@contract(x='array[N]', returns='array')
def normalize_pi(x):
    ''' Normalizes the entries in *x* in the interval :math:`[-pi,pi)`. '''
    x = np.array(x)
    angle = np.arctan2(np.sin(x), np.cos(x)) # in [-pi, pi]
    angle[angle == np.pi] = -np.pi
    return angle


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

@contract(s1='array[K],unit_length',
           s2='array[K],unit_length', returns='float,>=0,<=pi')
def geodesic_distance_on_sphere(s1, s2):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s1 == s2).all(): return 0.0
    dot_product = (s1 * s2).sum()
    return safe_arccos(dot_product)


@contract(S='directions', returns='float,>=0,<=pi')
def distribution_radius(S):
    ''' 
        Returns the radius of the given directions distribution.
        
        The radius is defined as the minimum *r* such that there exists a 
        point *s* in *S* such that all distances are within *r* from *s*. 
        
        .. math:: \\textsf{radius} = \\min \\{ r | \\exists s :  \\forall x \\in S : d(s,x) <= r \\}
    '''
    D = arccos(clip(dot(S.T, S), -1, 1))
    distances = D.max(axis=0)
    center = argmin(distances) 
    return distances[center]


@contract(S='array[3xK],directions', s='direction',
           returns='array[K](>=0,<=pi)')
def distances_from(S, s):
    ''' 
        Returns the geodesic distances on the sphere from a set of
        points *S* to a given point *s*. 
        
    '''
    return arccos(clip(dot(s, S), -1, 1))
    
    
@contract(ndim='(2|3),K', returns='array[K],unit_length')
def random_direction(ndim=3):
    '''
        Generates a random direction in :math:`\\sphere^{\\ndim-1}`. 
    
        Currently only implemented for 2D and 3D.
    '''
    if ndim == 3:
        z = uniform(-1, +1)
        t = uniform(0, 2 * pi)
        r = sqrt(1 - z ** 2)
        x = r * cos(t)
        y = r * sin(t)
        return array([x, y, z])
    elif ndim == 2:
        theta = uniform(0, 2 * pi)
        return array([cos(theta), sin(theta)])
        
    else: assert False, 'Not implemented'

@contract(N='int,>0,N', ndim="2|3", returns='array[3xN]')
def random_directions(N, ndim=3):
    ''' Returns a set of random directions. '''
    return vstack([random_direction(ndim) for i in range(N)]).T #@UnusedVariable

@contract(s='direction', returns='direction')
def any_distant_direction(s):
    ''' Returns a direction distant from both *s* and *-s*. '''
    z = default_axis()
    d = geodesic_distance_on_sphere(s, z)
    # TODO: make this a global parameter
    limit = 1.0 / 6.0 * pi 
    if min(d, pi - d) < limit:
        z = default_axis_orthogonal()
    return z

@contract(s='direction', returns='direction')
def any_orthogonal_direction(s):
    ''' Returns any axis orthogonal to *s* (not necessarily random). '''
    # choose a vector far away
    z = any_distant_direction(s)
    # z ^ s is orthogonal to s
    x = np.cross(z, s)
    v = x / norm(x)
    return v

@contract(s='array[K],unit_length,(K=2|K=3)', returns='array[K],unit_length')
def random_orthogonal_direction(s):
    ''' 
        Returns a random axis orthogonal to *s* 
        (only implemented for circle and sphere). 
    '''
    from .rotations import rot2d, rotation_from_axis_angle

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
    else: assert False, 'Not implemented'
    
    
@contract(s1='array[K],unit_length', s2='array[K],unit_length', t='number,>=0,<=1')
def slerp(s1, s2, t):
    ''' Spherical interpolation between two points on a hypersphere. '''    
    omega = arccos(dot(s1 / norm(s1), s2 / norm(s2)))
    so = sin(omega)
    if np.abs(so) < 1e-18: # XXX thresholds
        return s1
    return sin((1.0 - t) * omega) / so * s1 + sin(t * omega) / so * s2


@contract(ndim='(2|3),K',
           radius='number,>0,<=pi',
           num_points='int,>0',
           center='None|(array[K],unit_length)',
           returns='array[KxN],directions')
def random_directions_bounded(ndim, radius, num_points, center=None):
    '''
        Returns a random distribution of points in :math:`\\sphere^{\\ndim-1}`.
        within a certain radius from the point *center*. 
        
        The points will be distributed uniformly in that area of the sphere.
        If *center* is not passed, it will be a random direction. 
    '''
    from .rotations import rot2d, rotation_from_axis_angle

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

@contract(S='array[KxN],(K=2|K=3),directions', returns='array[KxN], directions')
def sorted_directions(S, num_around=15):
    ''' 
        Rearranges the directions in *S* in a better order for visualization.
    
        In 2D, sorts the directions using their angle. 
        
        In 3D, it tries to do a pleasant elicoidal arrangement 
        with **num_around** spires.
        
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
    
def sphere_area(r=1):
    ''' Returns the area of a sphere of the given radius. ''' 
    return 4 * pi * (r ** 2)

def spherical_cap_area(cap_radius):
    ''' 
        Returns the area of a spherical cap on the unit sphere 
        of the given radius. 
    
        See figure at http://mathworld.wolfram.com/SphericalCap.html
    '''
    h = 1 - cos(cap_radius)
    a = sin(cap_radius)
    A = pi * (a ** 2 + h ** 2)
    return A

def spherical_cap_with_area(cap_area):
    ''' 
        Returns the radius of a spherical cap of the given area. 
    
        See http://www.springerlink.com/content/3521h167300g7v62/
    '''
    A = cap_area
    L = sqrt(A / pi)
    h = L ** 2 / 2
    r = arccos(1 - h)
    return r

@contract(S='array[KxN],K>=2', returns='array[KxN]')
def project_vectors_onto_sphere(S, atol=1e-7):
    K, N = S.shape
    coords_proj = np.zeros((K, N))
    for i in range(N):
        v = S[:, i]
        nv = np.linalg.norm(v)
        if np.fabs(nv) < atol:
            raise ValueError('Vector too small: %s' % v)
        coords_proj[:, i] = v / nv
    return coords_proj

