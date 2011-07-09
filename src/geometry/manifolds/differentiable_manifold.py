from contracts import contract, all_disabled
from abc import ABCMeta, abstractmethod
from geometry import assert_allclose
from . import DoesNotBelong
from collections import namedtuple
from geometry.formatting import formatm
        
class DifferentiableManifold(object):
    ''' This is the base class for differentiable manifolds. ''' 
    __metaclass__ = ABCMeta
   
    def __init__(self):
        self._contained_in = {}
        self._contains = {}
        
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
        assert_allclose(proj, vx, atol=1e-8) #TODO: put somewhere else, class var
        # TODO: error
    
    def project_ts(self, base, v): # TODO: test
        '''
            Projects a vector *v_ambient* in the ambient space
            to the tangent space at point *base*.

            This function wraps some checks around :py:func:`project_ts_`, 
            which is implemented by the subclasses. 
        ''' 
        if not all_disabled():
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
        if not all_disabled():
            self.belongs(a)
            self.belongs(b)
        d = self.distance_(a, b)
        if not all_disabled():
            assert d >= 0
        return d
             
    def logmap(self, base, p):
        ''' 
            Computes the logarithmic map from base point *base* to target *b*. 
            
            This function wraps some checks around :py:func:`logmap_`, 
            which is implemented by the subclasses. 

            # XXX: what should we do in the case there is more than one logmap?
        '''
        if not all_disabled():
            self.belongs(base)
            self.belongs(p)
        v = self.logmap_(base, p)
        if not all_disabled():
            self.belongs_ts(base, v)
        return v

    def expmap(self, base, v):
        ''' 
            Computes the exponential map from *base* for the velocity vector *v*. 

            This function wraps some checks around :py:func:`expmap_`, 
            which is implemented by the subclasses. 
            
        '''
        if not all_disabled():
            self.belongs(base, 'Base point passed to expmap().')
            self.belongs_ts(base, v)
        
        p = self.expmap_(base, v)
        
        if not all_disabled():
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
        if not all_disabled():
            self.belongs(a)
            self.belongs(b)
        vel = self.logmap(a, b)
        vel2 = vel * t
        p = self.expmap(a, vel2)
        return p
    
    def friendly(self, a):
        ''' Returns a friendly description string for a point on the manifold. '''
        return "%s" % a 
    
    def assert_close(self, a, b, atol=1e-8, msg=None):
        ''' 
            Asserts that two points on the manifold are close to the given
            tolerance. 
        '''
        distance = self.distance(a, b)
        if msg is None: msg = ""
        if distance > atol:
            msg += "\nThe two points should be the same:\n"
            msg += "- a: %s\n" % self.friendly(a)
            msg += "- b: %s\n" % self.friendly(b)
            msg += formatm('a', a, 'b', b)
            assert_allclose(distance, 0, atol=atol, err_msg=msg)
        return distance
    
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
    
        
    ManifoldRelation = namedtuple('ManifoldEmbedding',
                                   'child parent embed_in project_from steps')
    def embed_relation(self, M, embed_in, project_from, steps=None):
        ''' Defines an embedding relation to a bigger manifold M. '''
        if M is self:
            raise ValueError('%s: Trying to add an embedding relationship to itself.' % 
                             self) 
        if steps is None:
            steps = [self, M]
        def format_steps(s):
            return '->'.join([x.__str__() for x in s])
        relation = self.ManifoldRelation(self, M, embed_in, project_from, steps)
        if M in self._contained_in:
            known_steps = self._contained_in[M].steps 
            if len(known_steps) <= len(steps):
                return
                #msg = ('Ignoring %s, I know %s)' % 
                #      (format_steps(steps), format_steps(known_steps)))
                # print(msg)
        self._contained_in[M] = relation
        M._contains[self] = relation
        
        # print('Created new relation: %s' % relation.steps)
        
        # Now, all our children can be embedded in M as well
        for child in self._contains:
            DifferentiableManifold.connect_via(child, self, M)
        
        for parent in M._contained_in:
            DifferentiableManifold.connect_via(self, M, parent)
            
    @staticmethod
    def connect_via(A, B, C):
        assert A.embeddable_in(B)  
        assert B.embeddable_in(C)  
        
        AB = A._contained_in[B]
        BC = B._contained_in[C]
        
        def AC_embed_in(a):
            b = AB.embed_in(a)
            c = BC.embed_in(b)
            return c
        def AC_project_from(c):
            b = BC.project_from(c)
            a = AB.project_from(b)
            return a
        new_steps = AB.steps + BC.steps[1:]
        A.embed_relation(C, AC_embed_in, AC_project_from, new_steps) 
         
    def embed_in(self, M, my_point):
        ''' Embeds a point on this manifold to the target manifold M. '''
        self.belongs(my_point)
        if not self.embeddable_in(M):
            msg = ('%s (%s) is not embeddable in %s (%s) (embeddable in %s)' % 
                   (self, id(self), M, id(M), self._contained_in.keys()))
            raise ValueError(msg)
        return self._contained_in[M].embed_in(my_point)
    
    def project_from(self, M, his_point):
        ''' Projects a point on a bigger manifold to this manifold. '''
        if not self.embeddable_in(M):
            msg = ('%s (%s) is not embeddable in %s (%s) (embeddable in %s)' % 
                   (self, id(self), M, id(M), self._contained_in.keys()))
            raise ValueError(msg)
        return self._contained_in[M].project_from(his_point)
        
    def project_to(self, m, my_point):
        if not self.can_represent(m):
            msg = ('%s does not contain %s (contains  %s)' % 
                   (self, m, self._contains.keys()))
            raise ValueError(msg)
        return self._contains[m].project_from(my_point)
    
    def can_represent(self, manifold):
        return manifold in self._contains
    
    def embeddable_in(self, manifold):
        return manifold in self._contained_in
    
    
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
        

    
