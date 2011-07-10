from . import (best_similarity_transform, contract, np, assert_allclose,
    project_vectors_onto_sphere)
from contracts import check_multiple
import itertools
import scipy.linalg



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


@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN]')
def inner_product_embedding_slow(C, ndim):
    U, S, V = np.linalg.svd(C, full_matrices=0)
    check_multiple([ ('array[NxN]', U),
                     ('array[N]', S),
                     ('array[NxN]', V) ])
    coords = V[:ndim, :]
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    return coords

@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN]')
def inner_product_embedding(C, ndim): 
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


def truncated_svd_randomized(M, k):
    ''' Truncated SVD based on randomized projections. '''
    p = k + 5
    Y = np.dot(M, np.random.normal(size=(M.shape[1], p)))
    Q, r = np.linalg.qr(Y) #@UnusedVariable
    B = np.dot(Q.T, M)
    Uhat, s, v = np.linalg.svd(B, full_matrices=False)
    U = np.dot(Q, Uhat)
    return U.T[:k].T, s[:k], v[:k]    

@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN]')
def inner_product_embedding_randomized(C, ndim): 
    ''' Best embedding of inner product matrix based on randomized projections. '''
    U, S, V = truncated_svd_randomized(C, ndim) #@UnusedVariable
    check_multiple([ ('K', ndim),
                     ('array[KxN]', V),
                     ('array[K]', S)  ])
    coords = V
    for i in range(ndim):
        coords[i, :] = coords[i, :]  * np.sqrt(S[i])
    return coords

@contract(D='array[MxM](>=0)', ndim='K,int,>=1', returns='array[KxM]')
def mds(D, ndim, embed=inner_product_embedding):
    diag = D.diagonal()
    assert_allclose(diag, 0)
    # Find centered cosine matrix
    P = D * D
    B = double_center(P)
    return embed(B, ndim)
 
@contract(D='array[MxM](>=0)', ndim='K,int,>=1', returns='array[KxM]')
def mds_randomized(D, ndim):
    ''' MDS based on randomized projections. '''
    return mds(D, ndim, embed=inner_product_embedding_randomized)
    
@contract(C='array[NxN]', ndim='int,>0,K', returns='array[KxN],directions')
def spherical_mds(C, ndim, embed=inner_product_embedding):
    # TODO: check cosines
    coords = embed(C, ndim)
    proj = project_vectors_onto_sphere(coords)
    return proj

# TODO: spherical_mds_randomized

best_embedding_on_sphere = spherical_mds



@contract(references='array[KxN]', distances='array[N](>=0)')
def place(references, distances):
    K, N = references.shape
    
    # First do MDS on all data
    D = np.zeros((N + 1, N + 1))
    D[:N, :N] = euclidean_distances(references)
    D[N, N] = 0
    D[N, :N] = distances
    D[:N, N] = distances
    Sm = mds(D, K)
    Dm = euclidean_distances(Sm)
  
    # Only if perfect  
    # assert_almost_equal(D[:N, :N], Dm[:N, :N])
    # new in other frame 
    R, t = best_similarity_transform(Sm[:, :N], references)
    
    Sm_aligned = np.dot(R, Sm) + t
    result = Sm_aligned[:, N]

    return result


