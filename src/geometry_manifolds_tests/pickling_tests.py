import pickle

from . import for_all_manifolds


@for_all_manifolds
def check_manifold_pickable(M):
    from io import BytesIO

    s = BytesIO()
    pickle.dump(M, s)

    # TODO: read
