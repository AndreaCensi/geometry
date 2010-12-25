import numpy as np

from contracts import new_contract, contracts, check, fail


@new_contract
@contracts(x='array[N],N>0')
def unit_length(x):
    return np.allclose(1, np.linalg.norm(x))

check('unit_length', np.array([1]))
check('unit_length', np.array([0, 1]))
fail('unit_length', np.array([0, 2]))

new_contract('direction', 'array[3], unit_length')
new_contract('unit_quaternion', 'array[4], unit_length')

@contracts(x='array[3x3], unit_length')
def direction(x):
    return np.allclose(np.linalg.det(x), 1)


@new_contract
@contracts(x='array[NxN],N>0')
def orthogonal(x):
#    N = orthogonal.context['N']
    N = x.shape[0]
    I = np.eye(N) 
    rtol = 10E-10
    atol = 10E-7
    np.testing.assert_allclose(I, np.dot(x, x.T), rtol=rtol, atol=atol)
    np.testing.assert_allclose(I, np.dot(x.T, x), rtol=rtol, atol=atol)
#    M = [np.dot(x, x.T), np.dot(x.T, x)]
#    return (np.allclose(I, M[0]) and
#            np.allclose(I, M[1]))  

@new_contract
@contracts(x='array[3x3], orthogonal')
def rotation_matrix(x):
    det = np.linalg.det(x)
    if not np.allclose(det, 1):
        raise ValueError('Determinant is not 1 (%f)' % det)
    
