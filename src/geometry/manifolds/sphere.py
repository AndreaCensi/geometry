from numpy.core.numeric import outer

from geometry import (geodesic_distance_on_sphere,
                      random_direction, normalize_length,
                      normalize_length_or_zero,
                      rotation_from_axis_angle, rot2d)


from . import DifferentiableManifold, np, assert_allclose, contract, check
from geometry.spheres import any_orthogonal_direction
                          
class Sphere(DifferentiableManifold):
    ''' These are hyperspheres of unit radius. '''
    
    norm_rtol = 1e-5
    atol_geodesic_distance = 1e-8
    
    @contract(order='(1|2)')
    def __init__(self, order):
        DifferentiableManifold.__init__(self)
        self.dimension = order + 1 
        
    def __repr__(self):
        return 'Sphere(%s)' % (self.dimension - 1)
                
    def distance_(self, a, b):
        return geodesic_distance_on_sphere(a, b)
         
    def logmap_(self, base, target):
        # XXX: what should we do in the case there is more than one logmap?
        d = geodesic_distance_on_sphere(target, base)
        if np.allclose(d, np.pi, atol=self.atol_geodesic_distance):
            if self.dimension == 2:
                xp = np.array([base[1], -base[0]])
            elif self.dimension == 3:
                xp = any_orthogonal_direction(base)
        else:
            x = target - base 
            xp = self.project_ts(base, x)
        xp = normalize_length_or_zero(xp)
        xp *= geodesic_distance_on_sphere(target, base)
        return xp
        
    def expmap_(self, base, vel):
        angle = np.linalg.norm(vel)
        if angle == 0: # XXX: tolerance
            return base
        
        if self.dimension == 2:
            dir = -np.sign(vel[0] * base[1] - base[0] * vel[1])
            R = rot2d(angle * dir)
            result = np.dot(R, base)
        elif self.dimension == 3:
            axis = -np.cross(normalize_length(vel), base)
            axis = normalize_length(axis)
            R = rotation_from_axis_angle(axis, angle)
            result = np.dot(R, base)
        else: assert False
        
        return result

    def project_ts_(self, base, x): # TODO: test
        P = np.eye(self.dimension) - outer(base, base)
        return np.dot(P, x)
        
    def belongs_(self, x):
        check('array[N]', x, 'Expected a vector.')
        assert_allclose(x.size, self.dimension,
                        err_msg='I expect a vector of size %d, got %s.' % 
                             (self.dimension, x))
        assert_allclose(1, np.linalg.norm(x), rtol=Sphere.norm_rtol)

    def sample_uniform(self):
        return random_direction(self.dimension)

    def interesting_points(self):
        if self.dimension == 2:
            points = []
            points.append(np.array([-1, 0]))
            points.append(np.array([0, 1]))
            points.append(np.array([0, -1]))
            points.append(np.array([+1, 0]))
            points.append(np.array([np.sqrt(2) / 2, np.sqrt(2) / 2]))
            return points
        else:
            points = []
            points.append(np.array([-1, 0, 0]))
            points.append(np.array([0, 1, 0]))
            points.append(np.array([0, 0, 1]))
            points.append(np.array([0, 0, -1]))
            points.append(np.array([np.sqrt(2) / 2, np.sqrt(2) / 2, 0]))
            return points
            
    def friendly(self, x):
        if self.dimension == 2:
            theta = np.arctan2(x[1], x[0])
            return 'Dir(%6.1fdeg)' % np.degrees(theta)
        elif self.dimension == 3:
            theta = np.arctan2(x[1], x[0])
            elevation = np.arcsin(x[2])
            return 'Dir(%6.1fdeg,el:%5.1fdeg)' % (np.degrees(theta),
                                                      np.degrees(elevation))
        else: assert False
        
