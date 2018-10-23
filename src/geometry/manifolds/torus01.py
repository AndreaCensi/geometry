# coding=utf-8
from contracts import contract
import numpy as np

from .differentiable_manifold import DifferentiableManifold
from .differentiable_manifold import RandomManifold

__all__ = ['TorusW', 'TorusW', 'Ts', 'Ts1', 'Ts2', 'Ts3']


class TorusW(RandomManifold):
    """ This is a torus whose coordinates wrap around in [0, W).
        All points in R^n belong to the torus.  """

    @contract(widths='seq[N](>0)', normalize_bias='None|seq[N](number)')
    def __init__(self, widths, normalize_bias=None):
        """
            :param normalize_bias: Only relevant for normalize(). If None, the normalization
            will be in [0,W[0]], [0,W[1]], etc. If given a bias, the normalization
            will be in [b[0],W[0]+b[0]], etc.
        """
        self.widths = np.array(widths, dtype='float')
        self.n = self.widths.size
        if normalize_bias is None:
            normalize_bias = np.zeros(self.n)
        self.normalize_bias = normalize_bias
        DifferentiableManifold.__init__(self, dimension=self.n)

    @contract(a='array[N]')
    def belongs(self, a):
        pass

    @contract(a='belongs', b='belongs', returns='>=0')  # returns='>=0,<0.8')
    def distance(self, a, b):
        _, vel = self.logmap(a, b)
        return np.linalg.norm(vel)

    def logmap(self, base, p):
        a1 = self.normalize(base)
        b1 = self.normalize(p)
        # printm('a1', a1)
        # printm('b1', b1)
        vel = b1 - a1  # between -self.widths[i] and +self.widths[i]
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
            wi = self.widths[i]
            if vel[i] > +wi / 2.0:
                vel[i] = vel[i] - wi
            elif vel[i] < -wi / 2.0:
                vel[i] = vel[i] + wi
        return base, vel

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        a, vel = bv
        # b = self.normalize(a + vel)
        b = a + vel
        return b

    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv):
        return bv  # XXX: more checks

    @contract(returns='belongs')
    def sample_uniform(self):
        return (np.random.rand(self.n) - 0.5) * 10 * self.widths

    @contract(returns='belongs_ts')
    def sample_velocity(self, a):  # @UnusedVariable
        vel = np.random.randn(self.n)
        vel = vel / np.linalg.norm(vel)  # XXX
        return vel

    def normalize(self, a):
        q = (a - self.normalize_bias) / self.widths
        y = q - np.floor(q)
        return y * self.widths + self.normalize_bias

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


Ts1 = TorusW([2], [-1])
Ts2 = TorusW([2, 2], [-1, -1])
Ts3 = TorusW([2, 2, 2], [-1, -1, -1])
Ts = {1: Ts1, 2: Ts2, 3: Ts1}
