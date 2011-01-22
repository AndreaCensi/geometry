from contracts import contracts
from abc import ABCMeta, abstractmethod
from snp_geometry import assert_allclose

class DoesNotBelong(Exception):
    def __init__(self, M, point, e, context=None):
        self.M = M
        self.point = point
        self.e = '%s' % e
        self.context = context
        
    def __str__(self):
        s = ''
        if self.context is not None:
            s += '%s\n' % self.context
        s += '%s: The point does not belong here: %s\n' % (self.M, self.point)
        s += self.e
        return s 
        
class DifferentiableManifold: 
    __metaclass__ = ABCMeta
   
    def belongs(self, x, msg=None):
        ''' Checks that a point belongs to this manifold. '''
        try:
            self._belongs(x)
        except Exception as e:
            raise DoesNotBelong(self, x, e, msg)

    def belongs_ts(self, base, vx):
        ''' Checks that a vector belongs to this manifold. '''
        proj = self.project_ts(base, vx)
        assert_allclose(proj, vx, atol=1e-8)
    
    def project_ts(self, base, v): # TODO: test
        ''' Projects a vector in the ambient space to a vector on the 
            tangent space. '''
        self.belongs(base)
        # check dimensions?
        v2 = self._project_ts(base, v)
        return v2
    
    
    def distance(self, a, b):
        ''' Returns the geodesic distance between two points. '''
        self.belongs(a)
        self.belongs(b)
        d = self._distance(a, b)
        assert d >= 0
        return d
             
    def logmap(self, base, p):
        ''' Returns the direction from base to target. '''
        self.belongs(base)
        self.belongs(p)
        v = self._logmap(base, p)
        self.belongs_ts(base, v)
        return v

    def expmap(self, base, v):
        ''' Inverse of logmap. '''
        self.belongs(base, 'Base point passed to expmap().')
        self.belongs_ts(base, v)
        p = self._expmap(base, v)
        self.belongs(p, 'Result of %s:_expmap(%s,%s)' % 
                        (self, self.friendly(base), v))
        return p
        
    
    
    def interesting_points(self):
        ''' Returns a list of "interesting points" on this manifold that
            should be used for testing various properties. 
        '''
        return []
    
    @contracts(t='>=0,<=1')
    def geodesic(self, a, b, t):
        ''' Returns the point along the geodesic. '''
        vel = self.logmap(a, b)
        vel2 = vel * t
        p = self.expmap(a, vel2)
        return p
    
    def friendly(self, a):
        ''' Returns a friendly description string for a point on the manifold. '''
        return "%s" % a 
    
    @abstractmethod
    def _belongs(self, a): pass
    @abstractmethod
    def _distance(self, a, b): pass
    @abstractmethod
    def _logmap(self, a, b): pass
    @abstractmethod
    def _expmap(self, a, b): pass
    @abstractmethod
    def _project_ts(self, base, vx): pass
    
    
class RandomManiold(DifferentiableManifold):
    @abstractmethod
    def sample_uniform(self):
        ''' Samples a random point in this manifold according to the Haar
            measure. Raises exception if the measure is improper (e.g., R^n). '''
    
    @abstractmethod
    def sample_velocity(self, a):
        ''' Samples a random velocity with length 1 at the base point a'''
        


class Group():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def multiply(self, g, h):
        ''' Implements the group operation. '''
        pass
    
    @abstractmethod
    def inverse(self, g):
        ''' Implements the group inversion. '''
        pass

    @abstractmethod
    def unity(self):
        ''' Returns the group unity. '''
        pass
        
class LieGroup(Group, DifferentiableManifold):
    # Add operations
    pass
        
    
    
    
