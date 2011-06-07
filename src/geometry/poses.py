from . import zeros, contract, assert_allclose, check, np, rot2d, new_contract
from .rotations import angle_from_rot2d


def check_SE(M):
    ''' Checks that the argument is in the special euclidean group. '''
    R, t, zero, one = extract_pieces(M) #@UnusedVariable
    check('SO', R)
    assert_allclose(one, 1)
    assert_allclose(zero, 0)

def check_se(M):
    ''' Checks that the input is in the special euclidean lie algebra. '''
    omega, v, Z, zero = extract_pieces(M) #@UnusedVariable
    check('so', omega)
    assert_allclose(Z, 0)
    assert_allclose(zero, 0)


new_contract('se', check_se)
new_contract('SE', check_SE)
new_contract('SE2', 'array[3x3], SE')
new_contract('se2', 'array[3x3], se')
new_contract('SE3', 'array[4x4], SE')
new_contract('se3', 'array[4x4], se')
    
    
@contract(x='array[NxN]', returns='tuple(array[MxM],array[M],array[M],number),M=N-1')
def extract_pieces(x):
    M = x.shape[0] - 1
    a = x[0:M, 0:M]
    b = x[0:M, M]
    c = x[M, 0:M]
    d = x[M, M]
    return a, b, c, d

@contract(a='array[MxM]', b='array[M]', c='array[M]', d='number', returns='array[NxN],N=M+1') 
def combine_pieces(a, b, c, d):
    M = a.shape[0]
    x = zeros((M + 1, M + 1)) 
    x[0:M, 0:M] = a
    x[0:M, M] = b
    x[M, 0:M] = c
    x[M, M] = d
    return x

@contract(R='array[NxN],SO', t='array[N]', returns='array[MxM],M=N+1,SE') 
def pose_from_rotation_translation(R, t):
    return combine_pieces(R, t, t * 0, 1)
    
@contract(pose='array[NxN],SE', returns='tuple(array[MxM], array[M]),M=N-1')
def rotation_translation_from_pose(pose):
    R, t, zero, one = extract_pieces(pose) #@UnusedVariable
    return R, t

    
@contract(t='array[2]|seq[2](number)', theta='number', returns='SE2')
def SE2_from_translation_angle(t, theta):
    ''' Returns an element of SE2 from translation and rotation. '''
    t = np.array(t)
    return combine_pieces(rot2d(theta), t, t * 0, 1)

@contract(pose='SE2', returns='tuple(array[2],float)')
def translation_angle_from_SE2(pose):
    R, t, zero, one = extract_pieces(pose) #@UnusedVariable
    return t, angle_from_rot2d(R)

# TODO: write tests for this, and other function
@contract(xytheta='array[3]|seq[3](number)', returns='SE2')
def SE2_from_xytheta(xytheta):
    ''' Returns an element of SE2 from translation and rotation. '''
    return SE2_from_translation_angle(xytheta[0:2], xytheta[2])


@contract(linear='array[2]|seq[2](number)', angular='number', returns='se2')
def se2_from_linear_angular(linear, angular):
    ''' Returns an element of se2 from linear and angular velocity. ''' 
    linear = np.array(linear)
    M = np.array([[0, -1], [+1, 0]]) * angular
    return combine_pieces(M, linear, linear * 0, 0)

@contract(vel='se2', returns='tuple(array[2],float)')
def linear_angular_from_se2(vel):
    M, v, Z, zero = extract_pieces(vel) #@UnusedVariable
    omega = M[1, 0]
    return v, omega







