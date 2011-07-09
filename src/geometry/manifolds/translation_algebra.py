from . import np, MatrixLieAlgebra
from contracts import contract
from geometry import extract_pieces, combine_pieces



class tran(MatrixLieAlgebra):
    ''' 
        lie algebra for translation
    '''
    
    @contract(n="1|2|3")
    def __init__(self, n):
        MatrixLieAlgebra.__init__(self, n + 1)
        
    def norm(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return np.linalg.norm(v)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return combine_pieces(W * 0, v, v * 0, 0)

    def __repr__(self):
        return 'tran(%s)' % (self.n - 1)
        
    def interesting_points(self):
        points = []
        points.append(self.zero())
        return points
