# coding=utf-8
from geometry.manifolds.tests import for_all_manifolds
import pickle

from six import BytesIO


@for_all_manifolds
def check_manifold_pickable(M):
    s = BytesIO()
    pickle.dump(M, s)

    # TODO: read

