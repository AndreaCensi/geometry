# coding=utf-8
from contracts import contract, describe_value, new_contract
from geometry import logger, logm, expm
import numpy as np

from .differentiable_manifold import DifferentiableManifold
from .group import Group

__all__ = ['MatrixLieGroup']


class MatrixLieGroup(Group, DifferentiableManifold):
    '''
        This is the base class for matrix Lie groups.

        Subclasses should provide a MatrixLieAlgebra
        object. Given the Lie algebra, we can compute everything.
        However, subclasses can choose to overload
        some functions if they know a more numerically stable implementation.

    '''

    def __init__(self, n, dimension, algebra):
        '''
            Initializes the Lie group.

            :param n: dimension of the matrix group.
            :param algebra: instance of :py:class:MatrixLieAlgebra
        '''
        DifferentiableManifold.__init__(self, dimension=dimension)
        self.n = n
        self.algebra = algebra
        assert self.algebra.n == self.n

        from .matrix_lie_group_tangent import MatrixLieGroupTangent
        self._tangent_bundle_algebra_rep = MatrixLieGroupTangent(self)

    def tangent_bundle(self):
        return self._tangent_bundle_algebra_rep

    def get_algebra(self):
        ''' Returns the interface to the corresponding Lie algebra. '''
        return self.algebra

    def unity(self):
        return np.eye(self.n)

    @contract(g='belongs', h='belongs')
    def multiply(self, g, h):
        return np.dot(g, h)

    @contract(g='belongs', returns='belongs')
    def inverse(self, g):
        try:
            #self.belongs(g)
            return np.linalg.inv(g)
        except:
            logger.error('Tried to invert %s' % describe_value(g))
            raise

    @new_contract
    def belongs_algebra(self, x):
        self.algebra.belongs(x)

    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv):
        '''
            Projects the vector *x* to the tangent space at point *base*.

            In the case of Lie Groups, we do this by translating the
            vector to the origin, projecting it to the Lie Algebra,
            and then translating it back.
        '''
        # get it to the origin
        base, vel = bv
        y = np.dot(self.inverse(base), vel)
        # project it to the algebra
        ty = self.algebra.project(y)
        # get it back where it belonged
        tty = np.dot(base, ty)
        return base, tty

    @contract(a='belongs', b='belongs')
    def distance(self, a, b):
        '''
            Computes the distance between two points.

            In the case of Lie groups, this is done by
            translating everything to the origin, computing the
            logmap, and using the norm defined in the Lie Algebra object.

        '''
#         x = self.multiply(a, self.inverse(b))
#         xt = self.algebra_from_group(x)
        _, vel = self.logmap(a, b)
        return self.algebra.norm(vel)

    @contract(base='belongs', p='belongs', returns='belongs_ts')
    def logmap(self, base, p):
        '''
            Returns the direction from base to target.

            In the case of Lie groups, this is implemented
            by using the usual matrix logarithm at the origin.

            Here the :py:func:`MatrixLieAlgebra.project` function
            is used to mitigate numerical errors.
        '''
        diff = self.multiply(self.inverse(base), p)
        X = self.algebra_from_group(diff)
        bX = np.dot(base, X)
        return (base, bX)

    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        '''
            This is the inverse of :py:func:`logmap_`.

            In the case of Lie groups, this is implemented using
            the usual matrix exponential.

            Here the :py:func:`MatrixLieAlgebra.project` function
            is used to mitigate numerical errors.
        '''
        base, vel = bv
        tv = np.dot(self.inverse(base), vel)
        tv = self.algebra.project(tv)
        x = self.group_from_algebra(tv)
        return np.dot(base, x)

    @contract(g='belongs', returns='belongs_algebra')
    def algebra_from_group(self, g):
        '''
            Converts an element of the group to the algebra.
            Uses generic matrix logarithm plus projection.
        '''
        X = np.array(logm(g).real)
        # mitigate numerical errors
        X = self.algebra.project(X)
        return X

    @contract(a='belongs_algebra', returns='belongs')
    def group_from_algebra(self, a):
        '''
            Converts an element of the algebra to the group.

            Uses generic matrix exponential.
        '''
        return expm(a)

    # TODO: write tests for this
    @contract(a='belongs', b='belongs', returns='belongs_ts')
    def velocity_from_points(self, a, b, delta=1):
        '''
            Find the velocity in local frame to go from *a* to *b* in
            *delta* time.
        '''
        x = self.multiply(self.inverse(a), b)
        xt = self.algebra_from_group(x)
#        xt = self.logmap(self.unity(), x) # XXX
#        xt = self.algebra.project(xt)
        return self.identity(), xt / delta

