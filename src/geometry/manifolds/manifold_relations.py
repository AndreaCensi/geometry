# coding=utf-8
from collections import defaultdict, namedtuple

__all__ = ['ManifoldRelations', 'Isomorphism', 'Embedding']

Isomorphism = namedtuple('Isomorphism',
                         'A B A_to_B B_to_A steps type desc')
Embedding = namedtuple('Embedding',
                       'A B A_to_B B_to_A steps type desc')


# Before: we used A._embedding[B]; now we use an external variable
# so that we use _IsomorphismRels[A][B]
class ManifoldRelations(object):
    _key_to_manifold = dict()
    _isomorphism_rels = defaultdict(dict)
    _embedding_rels = defaultdict(dict)
    _projection_rels = defaultdict(dict)

    @staticmethod
    def set_isomorphism(A, B, iso):
        assert iso.A == A
        assert iso.B == B
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        ManifoldRelations._isomorphism_rels[A][B] = iso

    @staticmethod
    def get_isomorphism(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return ManifoldRelations._isomorphism_rels[A][B]

    @staticmethod
    def exists_isomorphism(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return B in ManifoldRelations._isomorphism_rels[A]

    @staticmethod
    def all_isomorphisms(A):
        A = ManifoldRelations._get_key(A)
        return map(ManifoldRelations._manifold_from_key,
                   ManifoldRelations._isomorphism_rels[A].keys())

    # emabedding
    @staticmethod
    def set_embedding(A, B, em):
        assert em.A == A
        assert em.B == B
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        ManifoldRelations._embedding_rels[A][B] = em

    @staticmethod
    def get_embedding(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return ManifoldRelations._embedding_rels[A][B]

    @staticmethod
    def exists_embedding(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return B in ManifoldRelations._embedding_rels[A]

    @staticmethod
    def all_embeddings(A):
        A = ManifoldRelations._get_key(A)
        return map(ManifoldRelations._manifold_from_key,
                   ManifoldRelations._embedding_rels[A].keys())

    # projections
    @staticmethod
    def set_projection(A, B, proj):
        assert proj.A == A
        assert proj.B == B
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        ManifoldRelations._projection_rels[A][B] = proj

    @staticmethod
    def get_projection(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return ManifoldRelations._projection_rels[A][B]

    @staticmethod
    def exists_projection(A, B):
        A = ManifoldRelations._get_key(A)
        B = ManifoldRelations._get_key(B)
        return B in ManifoldRelations._projection_rels[A]

    @staticmethod
    def all_projections(A):
        A = ManifoldRelations._get_key(A)
        return map(ManifoldRelations._manifold_from_key,
                   ManifoldRelations._projection_rels[A].keys())

    @staticmethod
    def _get_key(M):
        """ Returns the string used for identifying a manifold """
        from .differentiable_manifold import DifferentiableManifold
        assert isinstance(M, DifferentiableManifold)
        k = str(M)
        if not k in ManifoldRelations._key_to_manifold:
            ManifoldRelations._key_to_manifold[k] = M
        return k

    @staticmethod
    def _manifold_from_key(k):
        M = ManifoldRelations._key_to_manifold[k]
        from .differentiable_manifold import DifferentiableManifold
        assert isinstance(M, DifferentiableManifold)
        return M

    @staticmethod
    def relations_descriptions(M):
        M = ManifoldRelations._get_key(M)
        _embedding = ManifoldRelations._embedding_rels[M]
        _isomorphism = ManifoldRelations._isomorphism_rels[M]
        _projection = ManifoldRelations._projection_rels[M]
        s = ('[= %s  >= %s  <= %s]' %
             (" ".join([str(a) for a in _isomorphism]),
              " ".join([str(a) for a in _projection]),
              " ".join([str(a) for a in _embedding])))
        return s

    @staticmethod
    def project(A, B, a_point):
        projection = ManifoldRelations.get_projection(A, B)
        x = projection.A_to_B(a_point)
        return x
