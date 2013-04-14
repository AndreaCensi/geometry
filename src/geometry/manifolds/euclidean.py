from . import (np, assert_allclose, contract, MatrixLinearSpace)


class Euclidean(MatrixLinearSpace):
    ''' 
        This is the usual Euclidean space of finite dimension;
        this is mostly used for debugging.
        
        There is no proper Haar measure; as an arbitrary choice,
        the :py:func:`sample_uniform`
        returns a sample from a Gaussian distribution centered at 0.
        
    '''
    
    def __init__(self, dimension):
        MatrixLinearSpace.__init__(self, dimension=dimension,
                                        shape=(dimension,))
    
    def __repr__(self):
        return 'R%s' % (self.dimension)

    @contract(x='array')
    def belongs(self, x):
        assert_allclose(x.size, self.dimension) 
        assert np.all(np.isreal(x)), "Expected real vector"

    def sample_uniform(self):
        return np.random.randn(self.dimension)

    def interesting_points(self):
        points = []
        points.append(np.zeros(self.dimension))
        points.append(np.ones(self.dimension))
        return points
    
    
    @contract(returns='belongs')
    def riemannian_mean(self, points):
        return np.mean(points, axis=0)
    
    def project(self, x): 
        return x
    
    
    def normalize(self, x):  # Used in diffeoplan
        return x
    
    
