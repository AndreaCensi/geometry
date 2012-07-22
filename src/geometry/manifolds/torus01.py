from . import DifferentiableManifold, np, contract
from geometry.manifolds.differentiable_manifold import RandomManifold


class Torus01(RandomManifold):
    """ This is a torus whose coordinates wrap around in [0, 1).
        All points in R^n belong to the torus.  """ 
    
    def __init__(self, n):
        DifferentiableManifold.__init__(self, dimension=n)
        self.n = n

    @contract(a='array[N]')
    def belongs(self, a):
        pass
#        
#        ok = np.logical_and(a >= 0, a < 1)
#        if not np.all(ok):
#            raise ValueError("Not all are ok in %s" % a)
        
    @contract(a='belongs', b='belongs', returns='>=0')#returns='>=0,<0.8')
    def distance(self, a, b):
        _, vel = self.logmap(a, b)
        return np.linalg.norm(vel)

    @contract(a='belongs', b='belongs', returns='belongs_ts')
    def logmap(self, a, b):
        a1 = self.normalize(a)
        b1 = self.normalize(b)
        vel = b1 - a1 # between -1 and +1
        # if any component v is |v| > 0.5, then we can reach the same
        # point in the other direction more efficiently
        # by using v' = 1-v
        # eg: a=0.8, b=0
        #     vel = -0.8
        #     vel' = vel + 1
        # eg: a=0, b=0.8
        #     vel = 0.8
        #     vel' = vel - 1
        # eg: a=0, b=0.75
        #     vel = 0.75
        #     vel' = vel - 1 = -.25
        
        for i in range(self.n):
            if vel[i] > 0.5:
                vel[i] = vel[i] - 1
            elif vel[i] < -0.5:
                vel[i] = vel[i] + 1
        return a, vel

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        a, vel = bv
        #b = self.normalize(a + vel)
        b = a + vel
        return b

    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv):
        return bv # XXX: more checks

    @contract(returns='belongs')
    def sample_uniform(self):
        return (np.random.rand(self.n) - 0.5) * 10

    @contract(returns='belongs_ts')
    def sample_velocity(self, a): #@UnusedVariable
        vel = np.random.randn(self.n)
        vel = vel / np.linalg.norm(vel) # XXX
        return vel

    @contract(x='array[N]', returns='array[N], belongs')
    def normalize(self, x):
        y = x - np.floor(x)
        return y 

    def friendly(self, a):
        return 'point(%s)' % a

    @contract(returns='list(belongs)')
    def interesting_points(self):
        interesting = []
        interesting.append(np.zeros(self.n))
        for _ in range(2): 
            interesting.append(self.sample_uniform())
        return interesting

    def __repr__(self):
        return 'Tn%s' % self.n


