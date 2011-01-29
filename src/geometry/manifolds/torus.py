from contracts import check
from . import DifferentiableManifold, np 
from geometry import normalize_pi

class Torus(DifferentiableManifold):

    def __init__(self, n):
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
