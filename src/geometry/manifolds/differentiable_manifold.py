from . import DoesNotBelong
from .. import assert_allclose, formatm
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from contracts import contract, all_disabled
from .. import printm
        
class DifferentiableManifold(object):
    ''' This is the base class for differentiable manifolds. ''' 
    __metaclass__ = ABCMeta
   
    def __init__(self, dimension): 
        self._isomorphisms = {}
        self._embedding = {}
        self._projection = {}
        self.dimension = dimension
        
        
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
    
    Isomorphism = namedtuple('Isomorphism', 'A B A_to_B B_to_A steps type desc')
    Embedding = namedtuple('Embedding', 'A B A_to_B B_to_A steps type desc')
    
    @staticmethod
    def isomorphism(A, B, A_to_B, B_to_A, type='user', steps=None, desc=None):
        if A.dimension != B.dimension:
            msg = ('You are trying to define an isomorphism'
                    ' between manifolds of different dimension:\n'
                    '- %s has dimension %d;\n'
                    '- %s has dimension %d.\n' % (A, A.dimension, B, B.dimension))
            raise ValueError(msg)
          
        Iso = DifferentiableManifold.Isomorphism
        if steps is None: steps = [(A, '~', B)]
        A._isomorphisms[B] = Iso(A, B, A_to_B, B_to_A, steps, type, desc)
        B._isomorphisms[A] = Iso(B, A, B_to_A, A_to_B, steps, type, desc)
    
    @staticmethod
    def embedding(A, B, A_to_B, B_to_A, type='user', steps=None, desc=None):
        if A.dimension > B.dimension:
            msg = ('You are trying to define an embedding'
                    ' from a large to a smaller manifold:\n'
                    '- %s has dimension %d;\n'
                    '- %s has dimension %d.\n' % (A, A.dimension, B, B.dimension))
            raise ValueError(msg)

        Embed = DifferentiableManifold.Embedding
        if steps is None: steps = [(A, '=', B)]
        A._embedding[B] = Embed(A, B, A_to_B, B_to_A, steps, type, desc)
        B._projection[A] = Embed(B, A, B_to_A, A_to_B, steps, type, desc)
  
        try:
            for a in A.interesting_points():
                A.belongs(a)
                b = A_to_B(a)
                B.belongs(b)    
        except:
            print('Invalid embedding:\n %s -> %s using %s' % (A, B, A_to_B))
            printm('a', a)
            raise
            
        try:
            for b in B.interesting_points():
                B.belongs(b)
                a = B_to_A(b)
                A.belongs(a)
        except:
            printm('b', b)
            print('Invalid embedding:\n %s <- %s using %s' % (A, B, B_to_A))
            raise
            
  
    def relations_descriptions(self):
        s = ('[= %s  >= %s  <= %s]' % 
                (" ".join([str(a) for a in self._isomorphisms]),
                    " ".join([str(a) for a in self._projection]),
                    " ".join([str(a) for a in self._embedding]))
            )
        return s
    
    def embed_in(self, M, my_point):
        ''' Embeds a point on this manifold to the target manifold M. '''
        self.belongs(my_point)
        if not self.embeddable_in(M):
            msg = ('%s is not embeddable in %s; %s' % 
                   (self, M, self.relations_descriptions()))
            raise ValueError(msg)
        x = self._embedding[M].A_to_B(my_point)
        M.belongs(x, msg='Error while embedding %s < %s point %s' % 
                  (self, M, my_point))
        return x
    
    def project_from(self, M, his_point):
        ''' Projects a point on a bigger manifold to this manifold. '''
        M.belongs(his_point)
        if not self.embeddable_in(M):
            msg = ('Cannot project from %s to %s; %s' % 
                   (self, M, self.relations_descriptions()))
            raise ValueError(msg)
        x = self._embedding[M].B_to_A(his_point)
        self.belongs(x)
        return x
    
    def project_to(self, m, my_point):
        self.belongs(my_point)
        if not self.can_represent(m):
            msg = ('%s does not contain %s; %s' % 
                   (self, m, self.relations_descriptions()))
            raise ValueError(msg)
        x = self._projection[m].A_to_B(my_point)
        m.belongs(x)
        return x

    def convert_to(self, m, my_point):
        self.belongs(my_point)
        if not  self.can_convert_to(m):
            msg = ('%s cannot be converted to %s; %s' % 
                   (self, m, self.relations_descriptions()))
            raise ValueError(msg)
        x = self._isomorphisms[m].A_to_B(my_point)
        m.belongs(x)
        return x

    def can_convert_to(self, manifold):
        return manifold in self._isomorphisms
    
    def can_represent(self, manifold): # XXX: change name
        return manifold in self._projection
    
    def embeddable_in(self, manifold):
        return manifold in self._embedding
    
    
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
        

    
