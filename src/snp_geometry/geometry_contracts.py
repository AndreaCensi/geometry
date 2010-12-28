import numpy as np

from contracts import new_contract, contracts
from .utils import assert_allclose

@new_contract
@contracts(x='array[N],N>0')
def unit_length(x):
    assert_allclose(1, np.linalg.norm(x))

new_contract('direction', 'array[3], unit_length')
new_contract('unit_quaternion', 'array[4], unit_length')

@new_contract
@contracts(x='array[NxN],N>0')
def orthogonal(x):
    N = x.shape[0]
    I = np.eye(N) 
    rtol = 10E-10
    atol = 10E-7
    assert_allclose(I, np.dot(x, x.T), rtol=rtol, atol=atol)
    assert_allclose(I, np.dot(x.T, x), rtol=rtol, atol=atol)

@new_contract
@contracts(x='array[3x3], orthogonal')
def rotation_matrix(x):
    det = np.linalg.det(x)
    assert_allclose(det, 1) 
    
