# coding=utf-8
from contracts import  contract
from geometry.spheres import normalize_pi
import numpy as np

from .differentiable_manifold import DifferentiableManifold

__all__ = ['Torus', 'T', 'T1', 'T2', 'T3']


class Torus(DifferentiableManifold):

    def __init__(self, n):
        DifferentiableManifold.__init__(self, dimension=n)
        self.n = n

    def belongs(self, a):
        ok = np.logical_and(a >= -np.pi, a < np.pi)
        if not np.all(ok):
            raise ValueError("Not all are ok in %s" % a)

    def distance(self, a, b):
        b = self.normalize(b - a)
        return np.linalg.norm(b)

    def logmap(self, base, p):
        vel = self.normalize(p - base)
        return base, vel

    def expmap(self, bv):
        a, vel = bv
        b = self.normalize(a + vel)
        return b

    def project_ts(self, bv):
        return bv  # XXX: more checks

    @contract(returns='belongs')
    def sample_uniform(self):
        return np.random.rand(self.n) * 2 * np.pi - np.pi

    def normalize(self, a):
        return normalize_pi(a)

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
        return 'T%s' % self.n


T1 = Torus(1)
T2 = Torus(2)
T3 = Torus(3)
T = {1: T1, 2: T2, 3: T3}
