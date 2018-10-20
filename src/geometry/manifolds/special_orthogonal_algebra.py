# coding=utf-8
from contracts import contract
from geometry.rotations import hat_map_2d, hat_map, map_hat_2d, map_hat
import numpy as np

from .matrix_lie_algebra import MatrixLieAlgebra

__all__ = ['so_algebra', 'so2', 'so3', 'so']


class so_algebra(MatrixLieAlgebra):
    '''
        This is the Lie algebra of skew-symmetric matrices so(n),
        for the Special Orthogonal group SO(n).
    '''

    def __init__(self, n):
        dimension = {2: 1, 3: 3}[n]
        MatrixLieAlgebra.__init__(self, n=n, dimension=dimension)

    def project(self, v):
        ''' Projects *v* to the closest skew-symmetric matrix. '''
        return 0.5 * (v - v.T)

    def __repr__(self):
        return 'so%s' % (self.n)

    def interesting_points(self):
        points = []
        points.append(self.zero())
        if self.n == 2:
            points.append(hat_map_2d(np.pi))
            points.append(hat_map_2d(np.pi / 2))
            points.append(hat_map_2d(-np.pi))
        elif self.n == 3:
            points.append(hat_map(np.array([0, 0, 1]) * np.pi / 2))
            points.append(hat_map(np.array([0, 0, 1]) * np.pi))
            points.append(hat_map(np.array([0, 1, 0]) * np.pi / 2))
            points.append(hat_map(np.array([0, 1, 0]) * np.pi))
            points.append(hat_map(np.array([1, 0, 0]) * np.pi / 2))
            points.append(hat_map(np.array([1, 0, 0]) * np.pi))
        else:
            assert False, 'Not implemented for n=%s' % self.n
        return points

    @contract(a='belongs')
    def vector_from_algebra(self, a):
        if self.n == 2:
            return np.array([map_hat_2d(a)])
        elif self.n == 3:
            return map_hat(a)
        else:
            assert False, 'Not implemented for n=%s.' % self.n

    @contract(v='array[N]')
    def algebra_from_vector(self, v):
        if self.n == 2:
            return hat_map_2d(v[0])
        elif self.n == 3:
            return hat_map(v)
        else:
            assert False, 'Not implemented for n=%s.' % self.n


so2 = so_algebra(2)
so3 = so_algebra(3)
so = {2: so2, 3: so3}
