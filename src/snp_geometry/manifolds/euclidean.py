from . import DifferentiableManifold, np, assert_allclose
from contracts import contracts

class Euclidean(DifferentiableManifold):
    
    def __init__(self, dimension):
        self.dimension = dimension
    
    def __repr__(self):
        return 'Euclidean(%s)' % (self.dimension)

    @contracts(x='array')
    def _belongs(self, x):
        assert_allclose(x.size, self.dimension) 
        assert np.all(np.isreal(x)), "Expected real vector"
        
    def _project_ts(self, base, x): # TODO: test @UnusedVariable
        return x
                    
    def _distance(self, a, b):
        return np.linalg.norm(a - b)
         
    def _logmap(self, base, target):
        return target - base
        
    def _expmap(self, base, vel):
        return base + vel

    def sample_uniform(self):
        return np.random.randn(self.dimension)

    def interesting_points(self):
        zero = np.zeros(self.dimension)
        return [zero] 
