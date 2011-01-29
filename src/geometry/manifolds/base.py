from contracts import contract
from abc import ABCMeta, abstractmethod
from geometry import assert_allclose

class DoesNotBelong(Exception):
    ''' Exception thrown when a point does not belong
        to a certain manifold *M*. '''
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
        
class DifferentiableManifold(object):
    ''' This is the base class for differentiable manifolds. ''' 
    __metaclass__ = ABCMeta
   
    def belongs(self, x, msg=None):
        ''' 
            Checks that a point belongs to this manifold.  
        
            This function wraps some checks around :py:func:`belongs_`, 
            which is implemented by the subclasses. 
        '''
        try:
            self.belongs_(x)
        except Exception as e:
            raise DoesNotBelong(self, x, e, msg)

    def belongs_ts(self, base, vx):
        ''' 
            Checks that a vector *vx* belongs to the tangent space
            at the given point *base*.

        '''
        proj = self.project_ts(base, vx)
        assert_allclose(proj, vx, atol=1e-8)
    
    def project_ts(self, base, v): # TODO: test
        '''
            Projects a vector *v_ambient* in the ambient space
            to the tangent space at point *base*.

            This function wraps some checks around :py:func:`project_ts_`, 
            which is implemented by the subclasses. 
        ''' 
        self.belongs(base)
        # check dimensions?
        v2 = self.project_ts_(base, v)
        return v2
    
    
    def distance(self, a, b):
        ''' 
            Computes the geodesic distance between two points. 

            This function wraps some checks around :py:func:`distance_`, 
            which is implemented by the subclasses. 
        '''
        self.belongs(a)
        self.belongs(b)
        d = self.distance_(a, b)
        assert d >= 0
        return d
             
    def logmap(self, base, p):
        ''' 
            Computes the logarithmic map from base point *base* to target *b*. 
            
            This function wraps some checks around :py:func:`logmap_`, 
            which is implemented by the subclasses. 

        '''
        self.belongs(base)
        self.belongs(p)
        v = self.logmap_(base, p)
        self.belongs_ts(base, v)
        return v

    def expmap(self, base, v):
        ''' 
            Computes the exponential map from *base* for the velocity vector *v*. 

            This function wraps some checks around :py:func:`expmap_`, 
            which is implemented by the subclasses. 
            
        '''
        self.belongs(base, 'Base point passed to expmap().')
        self.belongs_ts(base, v)
        p = self.expmap_(base, v)
        self.belongs(p, 'Result of %s:_expmap(%s,%s)' % 
                        (self, self.friendly(base), v))
        return p
        
    
    def interesting_points(self):
        ''' 
            Returns a list of "interesting points" on this manifold that
            should be used for testing various properties. 
        '''
        return []
    
    @contract(t='>=0,<=1')
    def geodesic(self, a, b, t):
        ''' Returns the point interpolated along the geodesic. '''
        self.belongs(a)
        self.belongs(b)
        vel = self.logmap(a, b)
        vel2 = vel * t
        p = self.expmap(a, vel2)
        return p
    
    def friendly(self, a):
        ''' Returns a friendly description string for a point on the manifold. '''
        return "%s" % a 
    
    @abstractmethod
    def belongs_(self, a): 
        ''' Checks that a point belongs to this manifold. '''  
    
    @abstractmethod
    def distance_(self, a, b): 
        ''' Computes the geodesic distance between two points. '''
        
    @abstractmethod
    def logmap_(self, a, b): 
        ''' Computes the logarithmic map from base point *a* to target *b*. '''
        
    @abstractmethod
    def expmap_(self, a, v):
        ''' Computes the exponential map from *a* for the velocity vector *v*. '''
        
    @abstractmethod
    def project_ts_(self, base, v_ambient):
        ''' 
            Projects a vector *v_ambient* in the ambient space
            to the tangent space at point *base*. 
        '''
    
    
class RandomManifold(DifferentiableManifold):
    ''' This is the base class for manifolds that have the ability 
        to sample points and vectors. '''
        
    @abstractmethod
    def sample_uniform(self):
        ''' Samples a random point in this manifold according to the Haar
            measure. Raises exception if the measure is improper (e.g., R^n). '''
    
    @abstractmethod
    def sample_velocity(self, a):
        ''' Samples a random velocity with length 1 at the base point a'''
        


class Group(object):
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
        
        
    
    
    
