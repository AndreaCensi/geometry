# coding=utf-8
from contracts import contract
from .differentiable_manifold import DifferentiableManifold

__all__ = ['TangentBundle']


class TangentBundle(DifferentiableManifold):
    ''' This class represents the tangent bundle of a generic manifold
        using a tuple (base, vel) where vel is tangent at base.

        (MatrixLieGroup has different representation)
    '''

    # TODO: create tests for all of this

    def __init__(self, base_manifold):
        self.base = base_manifold
        dimension = 2 * base_manifold.get_dimension()
        DifferentiableManifold.__init__(self, dimension=dimension)

    def __str__(self):
        return "T%s" % self.base

    def belongs(self, x):
        return self.base.belongs_ts(x)

    def belongs_ts(self, bv):
        # XXX: can we make it recursive?
        raise ValueError('Not supported')

    def project_ts(self, bv):  # TODO: test
        # XXX: can we make it recursive?
        raise ValueError('Not supported')

    @contract(a='belongs', b='belongs', returns='>=0')
    def distance(self, a, b):
        # TODO: make checks for this
        # TODO: implement
        raise ValueError('Not supported')

    @contract(base='belongs', p='belongs', returns='belongs_ts')
    def logmap(self, base, p):
        raise ValueError('Not supported')

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        raise ValueError('Not supported')

    @contract(returns='list(belongs)')
    def interesting_points(self):
        # TODO: write this
        return []

    @contract(a='belongs')
    def friendly(self, a):
        '''
            Returns a friendly description string for a point on the manifold.
        '''
        return "%s" % a

