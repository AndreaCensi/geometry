from . import DifferentiableManifold, np, contract
from .. import normalize_pi
from contracts import check

class Torus(DifferentiableManifold):

    def __init__(self, n):
        DifferentiableManifold.__init__(self, dimension=n)
        self.n = n

    def belongs(self, a):
        check('array[N](>=-pi,<pi)', a, N=self.n)

    @contract(a='belongs', b='belongs', returns='>=0')
    def distance(self, a, b):
        b = self.normalize(b - a)
        return np.linalg.norm(b)

    @contract(a='belongs', b='belongs', returns='belongs_ts')
    def logmap(self, a, b): 
        vel = self.normalize(b - a)
        return a, vel

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        a, vel = bv 
        b = self.normalize(a + vel)
        return b

    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv): 
        return bv # XXX: more checks
    
    @contract(returns='belongs')
    def sample_uniform(self):
        return np.random.rand(self.n) * 2 * np.pi - np.pi
    
    def normalize(self, x):
        return normalize_pi(x)
    
    def friendly(self, a):
        return 'point(%s)' % a
    
    @contract(returns='list(belongs)')
    def interesting_points(self):
        o = np.ones(self.n)
        return [np.zeros(self.n), o * -np.pi] 
    
    def __repr__(self):
        #return 'Torus(%s)' % self.n
        return 'T%s' % self.n
    
        
