# coding=utf-8
from abc import abstractmethod

from contracts import ContractsMeta, contract, new_contract
from geometry import GEOMETRY_DO_EXTRA_CHECKS, logger
from geometry.formatting import formatm, printm
from geometry.utils import check_allclose, assert_allclose

from .manifold_relations import Isomorphism, Embedding, ManifoldRelations

__all__ = ['DifferentiableManifold', 'RandomManifold']


class DifferentiableManifold(object):
    ''' This is the base class for differentiable manifolds. '''
    __metaclass__ = ContractsMeta

    def __init__(self, dimension):
        self.dimension = dimension

        self.atol_distance = 1e-8

        # Save reference, but do not create straight away.
        self._tangent_bundle = None

    @abstractmethod
    @new_contract
    def belongs(self, x):
        '''
            Raises an Exception if the point does not belong to this manifold.

            This function wraps some checks around :py:func:`belongs_`,
            which is implemented by the subclasses.
        '''

    @new_contract
    @contract(bv='tuple(belongs, *)')
    def belongs_ts(self, bv):
        '''
            Checks that a vector *vx* belongs to the tangent space
            at the given point *base*.

        '''
        bvp = self.project_ts(bv)
        assert_allclose(bv[1], bvp[1], atol=self.atol_distance)

    @abstractmethod
    @contract(bv='tuple(belongs, *)')
    def project_ts(self, bv):  # TODO: test
        '''
            Projects a vector *bv* in the ambient space
            to the tangent space at point *base*.
        '''

    @abstractmethod
    @contract(a='belongs', b='belongs', returns='>=0')
    def distance(self, a, b):
        '''
            Computes the geodesic distance between two points.
        '''

    # @contract(returns='DifferentiableManifold') # Circular ref
    def tangent_bundle(self):
        ''' Returns the manifold corresponding to the tangent bundle.
            The default gives a generic implementation.
            MatrixLieGroup have a different one.
        '''
        if self._tangent_bundle is None:
            from . import TangentBundle
            self._tangent_bundle = TangentBundle(self)
        return self._tangent_bundle

    @abstractmethod
    @contract(base='belongs', p='belongs', returns='belongs_ts')
    def logmap(self, base, p):
        '''
            Computes the logarithmic map from base point *base* to target *b*.
            # XXX: what should we do in the case there is more than one logmap?
        '''

    @abstractmethod
    @contract(bv='belongs_ts', returns='belongs')
    def expmap(self, bv):
        '''
            Computes the exponential map from *base* for the velocity
            vector *v*.

            This function wraps some checks around :py:func:`expmap_`,
            which is implemented by the subclasses.

        '''

    @contract(returns='list(belongs)')
    def interesting_points(self):
        '''
            Returns a list of "interesting points" on this manifold that
            should be used for testing various properties.
        '''
        return []

    @contract(a='belongs', b='belongs', t='>=0,<=1', returns='belongs')
    def geodesic(self, a, b, t):
        ''' Returns the point interpolated along the geodesic. '''
        bv = self.logmap(a, b)
        return self.expmap((bv[0], bv[1] * t))

    @contract(a='belongs', returns='belongs')
    def normalize(self, a):
        """ Normalizes the coordinates to the canonical representation
            for this manifold. See TorusW. """
        return a

    @contract(returns='belongs', points='list[>=1](belongs)')
    def riemannian_mean(self, points):
        """ TODO: work out exceptions """
        raise NotImplementedError
        # return np.mean(self.points, axis=0)

    @contract(a='belongs')
    def friendly(self, a):
        '''
            Returns a friendly description string for a point on the manifold.
        '''
        return a.__str__()

    @contract(a='belongs', b='belongs')
    def assert_close(self, a, b, atol=1e-8, msg=None):
        '''
            Asserts that two points on the manifold are close to the given
            tolerance.
        '''
        distance = self.distance(a, b)
        if msg is None:
            msg = ""
        if distance > atol:
            msg += "\nThe two points should be the same:\n"
            msg += "- a: %s\n" % self.friendly(a)
            msg += "- b: %s\n" % self.friendly(b)
            msg += formatm('a', a, 'b', b)
            check_allclose(distance, 0, atol=atol, err_msg=msg)
        return distance

    @staticmethod
    def isomorphism(A, B, A_to_B, B_to_A, itype='user', steps=None, desc=None):
        if A.dimension != B.dimension:
            msg = ('You are trying to define an isomorphism'
                    ' between manifolds of different dimension:\n'
                    '- %s has dimension %d;\n'
                    '- %s has dimension %d.\n' % (A, A.dimension,
                                                  B, B.dimension))
            raise ValueError(msg)

        if steps is None:
            steps = [(A, '~', B)]

        ManifoldRelations.set_isomorphism(A, B, Isomorphism(A, B, A_to_B, B_to_A, steps, itype, desc))
        ManifoldRelations.set_isomorphism(B, A, Isomorphism(B, A, B_to_A, A_to_B, steps, itype, desc))

    @staticmethod
    def embedding(A, B, A_to_B, B_to_A, itype='user', steps=None, desc=None):
        if A.dimension > B.dimension:
            msg = ('You are trying to define an embedding'
                    ' from a large to a smaller manifold:\n'
                    '- %s has dimension %d;\n'
                    '- %s has dimension %d.\n' % (A, A.dimension,
                                                  B, B.dimension))
            raise ValueError(msg)

        if steps is None:
            steps = [(A, '=', B)]
        ManifoldRelations.set_embedding(A, B, Embedding(A, B, A_to_B, B_to_A, steps, itype, desc))
        ManifoldRelations.set_projection(B, A, Embedding(B, A, B_to_A, A_to_B, steps, itype, desc))

        # TODO: move somewhere
        if False:
        # if development:
            try:
                for a in A.interesting_points():
                    A.belongs(a)
                    b = A_to_B(a)
                    B.belongs(b)
            except:
                print('Invalid embedding:\n %s -> %s using %s' % (A, B,
                                                                  A_to_B))
                printm('a', a)
                raise

            try:
                for b in B.interesting_points():
                    B.belongs(b)
                    a = B_to_A(b)
                    A.belongs(a)
            except:
                printm('b', b)
                print('Invalid embedding:\n %s <- %s using %s' %
                      (A, B, B_to_A))
                raise

    def relations_descriptions(self):
        return ManifoldRelations.relations_descriptions(self)

    @contract(my_point='belongs')
    def embed_in(self, M, my_point):
        ''' Embeds a point on this manifold to the target manifold M. '''
        # self.belongs(my_point)
        if not self.embeddable_in(M):
            msg = ('%s is not embeddable in %s; %s' %
                   (self, M, self.relations_descriptions()))
            raise ValueError(msg)

        try:
            embedding = ManifoldRelations.get_embedding(self, M)
            x = embedding.A_to_B(my_point)
            if GEOMETRY_DO_EXTRA_CHECKS:
                M.belongs(x)
        except:
            msg = ('Error while embedding %s < %s point %s' % (self, M, my_point))
            logger.error(msg)
            raise

        return x

    @contract(returns='belongs')
    def project_from(self, M, his_point):
        ''' Projects a point on a bigger manifold to this manifold. '''
        if not self.embeddable_in(M):
            msg = ('Cannot project from %s to %s; %s' %
                   (self, M, self.relations_descriptions()))
            raise ValueError(msg)
        embedding = ManifoldRelations.get_embedding(self, M)
        # I found it like this; why didn't I use projection?
        x = embedding.B_to_A(his_point)
        return x

    @contract(my_point='belongs')
    def project_to(self, m, my_point):
        if not self.can_represent(m):
            msg = ('%s does not contain %s; %s' %
                   (self, m, self.relations_descriptions()))
            raise ValueError(msg)

        return ManifoldRelations.project(self, m, my_point)

    @contract(my_point='belongs')
    def convert_to(self, m, my_point):
        if not  self.can_convert_to(m):
            msg = ('%s cannot be converted to %s; %s' %
                   (self, m, self.relations_descriptions()))
            raise ValueError(msg)
        isomorphism = ManifoldRelations.get_isomorphism(self, m)
        x = isomorphism.A_to_B(my_point)
        return x

    def can_convert_to(self, manifold):
        return ManifoldRelations.exists_isomorphism(self, manifold)

    def can_represent(self, manifold):  # XXX: change name
        return ManifoldRelations.exists_projection(self, manifold)

    def embeddable_in(self, manifold):
        return ManifoldRelations.exists_embedding(self, manifold)

    def get_dimension(self):
        ''' Returns the intrinsic dimension of this manifold. '''
        return self.dimension

    @contract(returns='belongs', yaml_structure='list|dict')
    def from_yaml(self, yaml_structure):
        ''' Recovers a value from a Yaml structure. '''
        # TODO: explicit check
        # TODO: add testing
        from geometry.yaml import from_yaml
        return from_yaml(yaml_structure)

    @contract(x='belongs')
    def to_yaml(self, x):
        # TODO: add testing
        from geometry.yaml import to_yaml
        return to_yaml('%s' % self, x)


class RandomManifold(DifferentiableManifold):
    ''' This is the base class for manifolds that have the ability
        to sample random points. '''

    @abstractmethod
    def sample_uniform(self):
        '''
            Samples a random point in this manifold according to the Haar
            measure. Raises exception if the measure is improper (e.g., R^n).
        '''

    @abstractmethod
    @contract(a='belongs')
    def sample_velocity(self, a):
        ''' Samples a random velocity with length 1 at the base point a'''

