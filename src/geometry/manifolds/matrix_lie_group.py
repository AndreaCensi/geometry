from . import np, DifferentiableManifold, Group
from .. import logm, expm, assert_allclose
from abc import abstractmethod

class MatrixLieAlgebra(DifferentiableManifold):
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
    
    
    def __init__(self, n, dimension):
        DifferentiableManifold.__init__(self, dimension=dimension)
        self.n = n
    
    @abstractmethod        
    def project(self, v): #@UnusedVariable
        ''' Projects a matrix onto this Lie Algebra. '''
        assert False
    
    def belongs_(self, v):
        ''' Checks that a vector belongs to this algebra. '''
        proj = self.project(v)
        assert_allclose(proj, v, atol=1e-8) # XXX: tol
        
    def norm(self, v): # XX
        ''' Return the norm of a vector in the algebra.
            This is used in :py:class:`MatrixLieGroup` to measure
            distances between points in the Lie group. 
        '''
        return np.linalg.norm(v, 2)
    
    def zero(self):
        ''' Returns the zero element for this algebra. '''
        return np.zeros((self.n, self.n))

    # Manifolds methods
    def distance_(self, a, b):
        return self.norm(a - b)
    
    def expmap_(self, base, vel):
        return base + vel
        
    def logmap_(self, base, target):
        return target - base
        
    def project_ts_(self, base, vx):
        return vx # XXX

class MatrixLieGroup(Group, DifferentiableManifold):
    ''' 
        This is the base class for matrix Lie groups.
        
        Subclasses should provide a MatrixLieAlgebra
        object. Given the Lie algebra, we can compute everything.
        However, subclasses can choose to overload
        some functions if they know a more numerically stable implementation. 
        
    '''
        
    def __init__(self, n, dimension, algebra):
        ''' 
            Initializes the Lie group.
            
            :param n: dimension of the matrix group.
            :param algebra: instance of :py:class:MatrixLieAlgebra 
        '''
        DifferentiableManifold.__init__(self, dimension=dimension)
        self.n = n
        self.algebra = algebra
        assert self.algebra.n == self.n
        
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
        xt = self.algebra_from_group(x)
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
        X = self.algebra_from_group(diff)
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
        x = self.group_from_algebra(tv)
        return np.dot(base, x)
    
    def algebra_from_group(self, g):
        ''' 
            Converts an element of the group to the algebra. 
            Uses generic matrix logarithm plus projection.
        ''' 
        X = np.array(logm(g).real)
        # mitigate numerical errors
        X = self.algebra.project(X)
        return X
        
    def group_from_algebra(self, a):
        ''' 
            Converts an element of the algebra to the group. 
        
            Uses generic matrix exponential.
        '''
        return expm(a)
        
    # TODO: write tests for this
    def velocity_from_points(self, a, b, delta=1):
        ''' 
            Find the velocity in local frame to go from *a* to *b* in 
            *delta* time. 
        '''
        x = self.multiply(self.inverse(a), b)
        xt = self.logmap(self.unity(), x) # XXX
        xt = self.algebra.project(xt)
        return xt / delta

    
    
