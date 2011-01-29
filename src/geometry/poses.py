from . import zeros, contract, assert_allclose, check

#@contract(x='array[NxN]', returns='tuple(array[MxM],array[M],array[M],number),M=N-1')
def extract_pieces(x):
    M = x.shape[0] - 1
    a = x[0:M, 0:M]
    b = x[0:M, M]
    c = x[M, 0:M]
    d = x[M, M]
    return a, b, c, d

#@contract(a='array[MxM]', b='array[M]', c='array[M]', d='number', returns='array[NxN],N=M+1') 
def combine_pieces(a, b, c, d):
    M = a.shape[0]
    x = zeros((M + 1, M + 1)) 
    x[0:M, 0:M] = a
    x[0:M, M] = b
    x[M, 0:M] = c
    x[M, M] = d
    return x

@contract(R='array[NxN],orthogonal', t='array[N]',
          returns='array[MxM],M=N+1') # todo: sorthogonal
def pose_from_rotation_translation(R, t):
    return combine_pieces(R, t, t * 0, 1)
    
@contract(pose='array[NxN]', returns='tuple(array[MxM], array[M]),M=N-1')
def rotation_translation_from_pose(pose):
    R, t, zero, one = extract_pieces(pose)
    check('orthogonal', R)
    assert_allclose(one, 1)
    assert_allclose(zero, 0)
    return R, t
