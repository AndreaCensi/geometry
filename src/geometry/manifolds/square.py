from . import DifferentiableManifold, np, contract
from geometry.manifolds.differentiable_manifold import RandomManifold


class Square(RandomManifold):
    """ A cube/square in [0, 1].
        All points in R^n belong to the torus.  """ 
    
    def __init__(self, n):
        DifferentiableManifold.__init__(self, dimension=n)
        self.n = n

    @contract(a='array[N]')
    def belongs(self, a):
        ok = np.logical_and(a >= 0, a <= 1)
        if not np.all(ok):
            raise ValueError("Not all are ok in %s" % a)
        
    @contract(a='belongs', b='belongs', returns='>=0')#returns='>=0,<0.8')
    def distance(self, a, b):
        _, vel = self.logmap(a, b)
        return np.linalg.norm(vel)

    @contract(a='belongs', b='belongs', returns='belongs_ts')
    def logmap(self, a, b): 
        vel = b - a 
        return a, vel

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        a, vel = bv
        b = a + vel
        return b

    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv):
        return bv # XXX: more checks

    @contract(returns='belongs')
    def sample_uniform(self):
        return np.random.rand(self.n)
 
    @contract(returns='belongs_ts')
    def sample_velocity(self, a): #@UnusedVariable
        b = self.sample_uniform(a)
        _, vel = self.logmap(a, b)
        return vel
    
    def friendly(self, a):
        return 'point(%s)' % a

    @contract(returns='list(belongs)')
    def interesting_points(self):
        interesting = []
        interesting.append(np.zeros(self.n))
        for i in range(self.n):
            z = np.zeros(self.n)
            z[i] = 1
            interesting.append(z)
        return interesting

    def __repr__(self):
        return 'Sq%s' % self.n


