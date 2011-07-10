from contracts import check
from . import DifferentiableManifold, np 
from .. import normalize_pi

class Torus(DifferentiableManifold):

    def __init__(self, n):
        DifferentiableManifold.__init__(self, dimension=n)
        self.n = n

    def belongs_(self, a):
        check('array[N](>=-pi,<pi)', a, N=self.n)

    def distance_(self, a, b):
        b = self.normalize(b - a)
        return np.linalg.norm(b)

    def logmap_(self, a, b): 
        vel = self.normalize(b - a)
        return vel

    def expmap_(self, a, vel): 
        b = self.normalize(a + vel)
        return b

    def project_ts_(self, base, vx): 
        return vx
    
    def sample_uniform(self):
        return np.random.rand(self.n) * 2 * np.pi - np.pi
    
    def normalize(self, x):
        return normalize_pi(x)
    
    def friendly(self, a):
        return 'point(%s)' % a
    
    def interesting_points(self):
        o = np.ones(self.n)
        return [np.zeros(self.n), o * -np.pi] 
    
    def __repr__(self):
        #return 'Torus(%s)' % self.n
        return 'T%s' % self.n
    
        
