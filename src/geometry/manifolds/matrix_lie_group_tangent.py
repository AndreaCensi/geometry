# coding=utf-8
from contracts import contract
from .differentiable_manifold import DifferentiableManifold
from .matrix_lie_group import MatrixLieGroup

__all__ = ['MatrixLieGroupTangent']


class MatrixLieGroupTangent(DifferentiableManifold):
    ''' This class represents the tangent bundle of a matrix Lie group
        using a tuble (base, v0), where v0 is in the algebra.

        Compare with the generic TangentBundle that uses the representation
        (base, vel) where vel is tangent at base (it holds that vel=base*v0).

        (MatrixLieGroup has different representation)
    '''
    # TODO: the tangent bundle of a matrix Lie group has more properties than
    # this.
    # TODO: create tests for all of this

    def __init__(self, base_group):
        assert isinstance(base_group, MatrixLieGroup)
        self.base = base_group
        dimension = 2 * base_group.get_dimension()
        DifferentiableManifold.__init__(self, dimension=dimension)

    def __str__(self):
        return "T%se" % self.base

    @contract(x='tuple[2]')
    def belongs(self, x):
        self.base.belongs(x[0])
        self.base.get_algebra().belongs(x[1])

    def belongs_ts(self, bv):
        # TODO: implement
        raise ValueError('Not supported')

    def project_ts(self, bv):  # TODO: test
        # TODO: implement
        raise ValueError('Not supported')

    @contract(a='belongs', b='belongs', returns='>=0')
    def distance(self, a, b):
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
        v = self.base.get_algebra().vector_from_algebra(a[1])
        return "V(%s,%s)" % (self.base.friendly(a[0]), v.tolist())

