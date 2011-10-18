from . import np, MatrixLieAlgebra, contract
from .. import extract_pieces, combine_pieces


class tran(MatrixLieAlgebra):
    ''' 
        lie algebra for translation
    '''
    
    @contract(n="1|2|3")
    def __init__(self, n):
        MatrixLieAlgebra.__init__(self, n + 1, dimension=n)
        
    def norm(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return np.linalg.norm(v)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return combine_pieces(W * 0, v, v * 0, 0)

    def __repr__(self):
        return 'tr%s' % (self.n - 1)
        
    def interesting_points(self):
        points = []
        points.append(self.zero())
        return points
       
    @contract(a='belongs')
    def vector_from_algebra(self, a):
        W, v, zero, zero = extract_pieces(a) #@UnusedVariable
        if v.shape == ():
            v = v.reshape(1)
        assert v.size == self.n - 1
        return v

    @contract(returns='belongs', v='array[K]')
    def algebra_from_vector(self, v):
        assert v.size == self.n - 1
        return combine_pieces(np.zeros((self.n - 1, self.n - 1)), v, v * 0, 0)
       
