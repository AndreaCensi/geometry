from . import LieGroup, np
from abc import abstractmethod
from snp_geometry import logm, expm

class MatrixLieGroup(LieGroup):
    def __init__(self, n):
        ''' 
            :param n: dimension of the matrix group. 
        '''
        self.n = n
        
    def unity(self):
        return np.eye(self.n)

    def multiply(self, g, h):
        return np.dot(g, h)
    
    def inverse(self, g):
        return np.linalg.inv(g)

    def _project_ts(self, base, x):  
        # get it to the origin
        y = np.dot(self.inverse(base), x)
        ty = self.project_lie_algebra(y)
        tty = np.dot(base, ty)
        return tty

    @abstractmethod
    def project_lie_algebra(self, vx):
        ''' Projects vx onto the Lie Algebra. '''
        pass
    
#    @abstractmethod
#    def liealgebra(self):
#        ''' Returns a list of matrices representing an orthonormal
#            base for the Lie Algebra of this group. '''
#        pass    

    def _distance(self, a, b):
        x = self.multiply(a, self.inverse(b))
        xt = self.logmap(self.unity(), x)
        return np.linalg.norm(xt, 2)
         
    def _logmap(self, base, target):
        ''' Returns the direction from base to target. '''
        diff = self.multiply(self.inverse(base), target)
        X = np.array(logm(diff).real)
        return np.dot(base, X)

    def _expmap(self, base, vel):
        return np.dot(base, expm(vel))
