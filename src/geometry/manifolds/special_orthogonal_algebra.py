from . import  np, MatrixLieAlgebra
from .. import (hat_map, hat_map_2d)


class so_algebra(MatrixLieAlgebra):
    ''' 
        This is the Lie algebra of skew-symmetric matrices so(n),
        for the Special Orthogonal group SO(n).
    '''    
    
    def __init__(self, N):
        dimension = {2:1, 3:2}[N]
        MatrixLieAlgebra.__init__(self, n=N, dimension=dimension)
    
    def project(self, v):
        ''' Projects *v* to the closest skew-symmetric matrix. '''
        return 0.5 * (v - v.T)
    
    def __repr__(self):
        #return 'so(%s)' % (self.n)
        return 'so%s' % (self.n)

    def interesting_points(self):
        points = []
        points.append(self.zero())
        if self.n == 2:
            points.append(hat_map_2d(np.pi))
            points.append(hat_map_2d(np.pi / 2))
            points.append(hat_map_2d(-np.pi))
        if self.n == 3:
            points.append(hat_map(np.array([0, 0, 1]) * np.pi / 2))
            points.append(hat_map(np.array([0, 0, 1]) * np.pi))
            points.append(hat_map(np.array([0, 1, 0]) * np.pi / 2))
            points.append(hat_map(np.array([0, 1, 0]) * np.pi))
            points.append(hat_map(np.array([1, 0, 0]) * np.pi / 2))
            points.append(hat_map(np.array([1, 0, 0]) * np.pi))
    
        return points
    
