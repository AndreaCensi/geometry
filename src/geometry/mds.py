import itertools
import scipy.linalg
from contracts import check_multiple

from .basic_utils import contract, np, assert_allclose
from .spheres import project_vectors_onto_sphere


@contract(S='array[KxN]', returns='array[NxN](>=0)')
def euclidean_distances(S):
    ''' Computes the euclidean distance matrix for the given points. '''
    K, N = S.shape
    D = np.zeros((N, N))
    for i in range(N):
        p = S[:, i]
        pp = np.tile(p, (N, 1)).T
        assert pp.shape == (K, N)
        d2 = ((S - pp) * (S - pp)).sum(axis=0)
        d2 = np.maximum(d2, 0)
        D[i, :] = np.sqrt(d2)
    return D

def double_center(P):
    n = P.shape[0]
    
    grand_mean = P.mean()
    row_mean = np.zeros(n)
    col_mean = np.zeros(n)
    for i in range(n):
        row_mean[i] = P[i, :].mean()
        col_mean[i] = P[:, i].mean()
        
    
    R = row_mean.reshape(n, 1).repeat(n, axis=1)
    assert R.shape == (n, n)
    C = col_mean.reshape(1, n).repeat(n, axis=0)
    assert C.shape == (n, n)
    
    B2 = -0.5 * (P - R - C + grand_mean) 
    
    if False:
        B = np.zeros(P.shape)
        for i, j in itertools.product(range(n), range(n)):
            B[i, j] = -0.5 * (P[i, j] - col_mean[j] - row_mean[i] + grand_mean)
        assert_allclose(B2, B)
    
    return B2


@contract(D='array[MxM](>=0)', ndim='K,int,>=1', returns='array[KxM]')
def mds(D, ndim):
    diag = D.diagonal()
    assert_allclose(diag, 0)
    # Find centered cosine matrix
    P = D * D
    B = double_center(P)
    return best_embedding(B, ndim)


@contract(R='array[NxN]', ndim='int,>0,K', returns='array[KxN],directions')
def best_embedding_on_sphere(R, ndim):
    coords = best_embedding(R, ndim)
    proj = project_vectors_onto_sphere(coords)
    return proj

@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN]')
def best_embedding_slow(C, ndim):
    U, S, V = np.linalg.svd(C, full_matrices=0)
    check_multiple([ ('array[NxN]', U),
                     ('array[N]', S),
                     ('array[NxN]', V) ])
    coords = V[:ndim, :]
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    return coords

@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN]')
def best_embedding(C, ndim): 
    n = C.shape[0]
    eigvals = (n - ndim, n - 1)
    S, V = scipy.linalg.eigh(C, eigvals=eigvals)
    
    check_multiple([ ('K', ndim),
                     ('array[NxK]', V),
                     ('array[K]', S)  ])
    coords = V.T
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    return coords
 
