# coding=utf-8
from contracts import contract
from geometry.poses import extract_pieces, combine_pieces
import numpy as np

from .matrix_lie_algebra import MatrixLieAlgebra

__all__ = ['trana', 'tran', 'tran1', 'tran2', 'tran3']


class trana(MatrixLieAlgebra):
    '''
        lie algebra for translation
    '''

    @contract(n="1|2|3")
    def __init__(self, n):
        MatrixLieAlgebra.__init__(self, n + 1, dimension=n)

    def norm(self, X):
        W, v, zero, zero = extract_pieces(X)  # @UnusedVariable
        return np.linalg.norm(v)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X)  # @UnusedVariable
        return combine_pieces(W * 0, v, v * 0, 0)

    def __repr__(self):
        return 'tr%s' % (self.n - 1)

    def interesting_points(self):
        points = []
        points.append(self.zero())
        return points

    @contract(a='belongs')
    def vector_from_algebra(self, a):
        W, v, zero, zero = extract_pieces(a)  # @UnusedVariable
        if v.shape == ():
            v = v.reshape(1)
        assert v.size == self.n - 1
        return v

    @contract(returns='belongs', v='array[K]')
    def algebra_from_vector(self, v):
        assert v.size == self.n - 1
        return combine_pieces(np.zeros((self.n - 1, self.n - 1)), v, v * 0, 0)


tran1 = trana(1)
tran2 = trana(2)
tran3 = trana(3)
tran = {1: tran1, 2: tran2, 3: tran3}
