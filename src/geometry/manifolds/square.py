# coding=utf-8
from contracts import contract
from geometry.manifolds import DifferentiableManifold, RandomManifold
import numpy as np

__all__ = ['Square', 'Sq', 'Sq1', 'Sq2', 'Sq3']


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

    def distance(self, a, b):
        _, vel = self.logmap(a, b)
        return np.linalg.norm(vel)

    def logmap(self, base, p):
        vel = p - base
        return base, vel

    def expmap(self, bv):
        a, vel = bv
        b = a + vel
        return b

    def project_ts(self, bv):
        return bv  # XXX: more checks

    def sample_uniform(self):
        return np.random.rand(self.n)

    @contract(returns='belongs_ts')
    def sample_velocity(self, a):  # @UnusedVariable
        b = self.sample_uniform()
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


Sq1 = Square(1)
Sq2 = Square(2)
Sq3 = Square(3)
Sq = {1: Sq1, 2: Sq2, 3: Sq3}
