from . import np, MatrixLieAlgebra, so
from geometry import extract_pieces, combine_pieces

class se_algebra(MatrixLieAlgebra):
    ''' This is the Lie algebra se(n) for the Special Euclidean group SE(n). 
    
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''
    
    def __init__(self, n, alpha):
        MatrixLieAlgebra.__init__(self, n + 1)
        self.alpha = alpha
        self.son = so[n]
        
    def norm(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return np.linalg.norm(v) + self.alpha * self.son.norm(W)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        W = self.son.project(W)
        return combine_pieces(W, v, v * 0, 0)

    def __repr__(self):
        return 'se(%s)' % (self.n - 1)
        


