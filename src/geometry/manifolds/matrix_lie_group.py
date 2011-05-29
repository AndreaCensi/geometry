from . import np
from abc import abstractmethod, ABCMeta
from geometry import logm, expm, assert_allclose
from .base import DifferentiableManifold, Group

class MatrixLieAlgebra(object):
    ''' This is the base class for Matrix Lie Algebra.
    
        It is understood that it is composed by square matrices.
        
        The only function that *has* to be implemented is the 
        :py:func:`project` function that projects a square matrix
        onto the algebra. This function is used both for checking
        that a vector is in the algebra (see :py:func:`belongs`)
        and to mitigate the numerical errors.
        
        You probably also want to implement :py:func:`norm` if
        the default is not what you want.  
    '''
    __metaclass__ = ABCMeta
    
    
    def __init__(self, n):
        self.n = n
    
    @abstractmethod        
    def project(self, v): #@UnusedVariable
        ''' Projects a matrix onto this Lie Algebra. '''
        assert False
    
    def belongs(self, v):
        ''' Checks that a vector belongs to this algebra. '''
        proj = self.project(v)
        assert_allclose(proj, v, atol=1e-8) # XXX: tol
        
    def norm(self, v): # XX
        ''' Return the norm of a vector in the algebra.
            This is used in :py:class:`MatrixLieGroup` to measure
            distances between points in the Lie group. 
        '''
        return np.linalg.norm(v, 2)

class MatrixLieGroup(Group, DifferentiableManifold):
    ''' 
        This is the base class for matrix Lie groups.
        
        Subclasses should provide a MatrixLieAlgebra
        object. Given the Lie algebra, we can compute everything.
        However, subclasses can choose to overload
        some functions if they know a more numerically stable implementation. 
        
    '''
        
    def __init__(self, n, algebra):
        ''' 
            Initializes the Lie group.
            
            :param n: dimension of the matrix group.
            :param algebra: instance of :py:class:MatrixLieAlgebra 
        '''
        self.n = n
        self.algebra = algebra
        
    def unity(self):
        return np.eye(self.n)

    def multiply(self, g, h):
        return np.dot(g, h)
    
    def inverse(self, g):
        return np.linalg.inv(g)

    def project_ts_(self, base, x):
        ''' 
            Projects the vector *x* to the tangent space at point *base*.
        
            In the case of Lie Groups, we do this by translating the
            vector to the origin, projecting it to the Lie Algebra,
            and then translating it back. 
        '''
        # get it to the origin
        y = np.dot(self.inverse(base), x)
        # project it to the algebra
        ty = self.algebra.project(y)
        # get it back where it belonged
        tty = np.dot(base, ty)
        return tty 

    def distance_(self, a, b):
        ''' 
            Computes the distance between two points.
        
            In the case of Lie groups, this is done by 
            translating everything to the origin, computing the
            logmap, and using the norm defined in the Lie Algebra object.

        '''
        x = self.multiply(a, self.inverse(b))
        xt = self.logmap(self.unity(), x)
        return self.algebra.norm(xt)
        
    def logmap_(self, base, target):
        ''' 
            Returns the direction from base to target. 
        
            In the case of Lie groups, this is implemented
            by using the usual matrix logarithm at the origin.
            
            Here the :py:func:`MatrixLieAlgebra.project` function
            is used to mitigate numerical errors. 
        '''
        diff = self.multiply(self.inverse(base), target)
        X = np.array(logm(diff).real)
        # mitigate numerical errors
        X = self.algebra.project(X)
        return np.dot(base, X)

    def expmap_(self, base, vel):
        ''' 
            This is the inverse of :py:func:`logmap_`. 
        
            In the case of Lie groups, this is implemented using
            the usual matrix exponential.

            Here the :py:func:`MatrixLieAlgebra.project` function
            is used to mitigate numerical errors. 
        '''
        tv = np.dot(self.inverse(base), vel)
        tv = self.algebra.project(tv)
        x = expm(tv)
        return np.dot(base, x)
    
    # TODO: write tests for this
    def velocity_from_points(self, a, b, delta=1):
        ''' 
            Find the velocity in local frame to go from *a* to *b* in 
            *delta* time. 
        '''
        x = self.multiply(self.inverse(a), b)
        xt = self.logmap(self.unity(), x)
        xt = self.algebra.project(xt)
        return xt / delta

    
    
