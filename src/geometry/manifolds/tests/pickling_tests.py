from geometry.manifolds.tests import for_all_manifolds
from StringIO import StringIO
import pickle

@for_all_manifolds
def check_manifold_pickable(M):
    s = StringIO()
    pickle.dump(M, s)

    # TODO: read
    
