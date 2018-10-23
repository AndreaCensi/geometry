# coding=utf-8
from contracts import contract
from geometry.manifolds.differentiable_manifold import DifferentiableManifold


class NonCompactStiefel(DifferentiableManifold):
    ''' INCOMPLETE -- Matrices of fixed rank. '''

    @contract(n='N,N>0', p='P,P>0,P<=N')
    def __init__(self, p, n):
        '''
            Initializes the manifold structure.

            :param n: dimension of space
            :param p: rank of subspace
        '''
        DifferentiableManifold.__init__(self, 42)
        self.n = n
        self.p = p

    def belongs(self, a):
        assert False

    def distance(self, a, b):
        assert False

    def logmap(self, a, b):
        assert False

    def expmap(self, a, vel):
        assert False

    def project_ts(self, base, vx):
        assert False

    def sample_uniform(self):
        assert False

    def normalize(self, x):
        assert False

