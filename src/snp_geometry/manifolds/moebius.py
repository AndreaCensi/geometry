from contracts import check
from . import DifferentiableManifold, np 
from snp_geometry import normalize_pi

class Moebius(DifferentiableManifold):

    def __init__(self, n):
        self.n = n

    def _belongs(self, a):
        pass

    def _distance(self, a, b):
        pass

    def _logmap(self, a, b): 
        pass

    def _expmap(self, a, vel): 
        pass

    def _project_ts(self, base, vx): 
        pass
    
    def sample_uniform(self):
        pass
    
    def normalize(self, x):
        pass

