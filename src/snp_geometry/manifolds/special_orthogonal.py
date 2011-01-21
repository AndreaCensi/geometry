from . import MatrixLieGroup, np
from snp_geometry import  assert_allclose
from contracts import contracts
from snp_geometry import  rot2d, random_rotation
from contracts.main import check
from snp_geometry.rotations import axis_angle_from_rotation

class SO(MatrixLieGroup):
    
    @contracts(n='int,(2|3)')
    def __init__(self, n):
        MatrixLieGroup.__init__(self, n)

    def __repr__(self):
        return 'SO(%s)' % (self.n)

    def project_lie_algebra(self, vx):
        ''' Projects onto the Lie Algebra of SO(n): skew-symmetric matrices. '''
        return 0.5 * (vx - vx.T)
    
    def _belongs(self, x):
        check('orthogonal', x)
        det = np.linalg.det(x)
        assert_allclose(det, 1, err_msg='I expect the determinant to be +1.') 

    def sample_uniform(self):
        if self.n == 2:
            theta = np.random.rand() * np.pi
            return rot2d(theta)
        elif self.n == 3:
            return random_rotation()
        else:
            assert False, 'Not implemented for n>=4.'
            
    def friendly(self, x):
        if self.n == 2:
            theta = np.arctan2(x[1, 0], x[0, 0])
            return 'Rot(%.1fdeg)' % np.degrees(theta)
        elif self.n == 3:
            axis, angle = axis_angle_from_rotation(x)
            return 'Rot(%.1fdeg, %s)' % (np.degrees(angle), axis)
        else:
            assert False, 'Not implemented for n>=4.'
        
                
    
