from . import DifferentiableManifold, np, assert_allclose, contract


class Euclidean(DifferentiableManifold):
    ''' 
        This is the usual Euclidean space of finite dimension;
        this is mostly used for debugging.
        
        There is no proper Haar measure; as an arbitrary choice,
        the :py:func:`sample_uniform`
        returns a sample from a Gaussian distribution centered at 0.
        
    '''
    
    def __init__(self, dimension):
        DifferentiableManifold.__init__(self, dimension=dimension)
        self.dimension = dimension
    
    def __repr__(self):
        #return 'R(%s)' % (self.dimension)
        return 'R%s' % (self.dimension)

    @contract(x='array')
    def belongs_(self, x):
        assert_allclose(x.size, self.dimension) 
        assert np.all(np.isreal(x)), "Expected real vector"
        
    def project_ts_(self, base, x): # TODO: test @UnusedVariable
        return x
                    
    def distance_(self, a, b):
        return np.linalg.norm(a - b)
         
    def logmap_(self, base, target):
        return target - base
        
    def expmap_(self, base, vel):
        return base + vel

    def sample_uniform(self):
        return np.random.randn(self.dimension)

    def interesting_points(self):
        points = []
        points.append(np.zeros(self.dimension))
        points.append(np.ones(self.dimension))
        return points
    
