# coding=utf-8
import pickle

from geometry.manifolds.tests import for_all_manifolds


@for_all_manifolds
def check_manifold_pickable(M):
    from six import BytesIO

    s = BytesIO()
    pickle.dump(M, s)

    # TODO: read
