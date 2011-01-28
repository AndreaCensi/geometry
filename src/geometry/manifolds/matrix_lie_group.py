from . import LieGroup, np
from abc import abstractmethod
from geometry import logm, expm, assert_allclose

class MatrixLieAlgebra(object):
    def __init__(self, n):
        self.n = n
    @abstractmethod        
    def project(self, v):
        pass 
    
    def belongs(self, v):
        ''' Checks that a vector belongs to this manifold. '''
        proj = self.project(v)
        assert_allclose(proj, v, atol=1e-8)
        
    def norm(self, v): # XXX
        return np.linalg.norm(v, 2)

class MatrixLieGroup(LieGroup):
    def __init__(self, n, algebra):
        ''' 
            :param n: dimension of the matrix group. 
        '''
        self.n = n
        self.algebra = algebra
        
    def unity(self):
        return np.eye(self.n)

    def multiply(self, g, h):
        return np.dot(g, h)
    
    def inverse(self, g):
        return np.linalg.inv(g)

    def _project_ts(self, base, x):  
        # get it to the origin
        y = np.dot(self.inverse(base), x)
        ty = self.algebra.project(y)
        tty = np.dot(base, ty)
        return tty 

    def _distance(self, a, b):
        x = self.multiply(a, self.inverse(b))
        xt = self.logmap(self.unity(), x)
        return self.algebra.norm(xt)
        
    def _logmap(self, base, target):
        ''' Returns the direction from base to target. '''
        diff = self.multiply(self.inverse(base), target)
        X = np.array(logm(diff).real)
        X = self.algebra.project(X)
        return np.dot(base, X)

    def _expmap(self, base, vel):
        tv = np.dot(self.inverse(base), vel)
        tv = self.algebra.project(tv)
        x = expm(tv)
        return np.dot(base, x)
    
    
    
