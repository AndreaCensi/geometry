from contracts import contract, check

from geometry import  (assert_allclose,
                           rot2d, random_rotation, axis_angle_from_rotation)

from . import MatrixLieGroup, np, MatrixLieAlgebra, S2


class so(MatrixLieAlgebra):
    ''' 
        This is the Lie algebra of skew-symmetric matrices so(n),
        for the Special Orthogonal group SO(n).
    '''    
    
    def project(self, v):
        ''' Projects *v* to the closest skew-symmetric matrix. '''
        return 0.5 * (v - v.T)
    
    def __repr__(self):
        return 'so(%s)' % (self.n)

class SO(MatrixLieGroup):
    ''' 
        This is the Special Orthogonal group SO(n) describing rotations
        of Euclidean space; implemented for n=2,3.
        
    '''
    
    @contract(n='int,(2|3)')
    def __init__(self, n):
        algebra = so(n)
        MatrixLieGroup.__init__(self, n, algebra)

    def __repr__(self):
        return 'SO(%s)' % (self.n)
    
    def belongs_(self, x):
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
            axisf = S2.friendly(axis)
            return 'Rot(%.1fdeg, %s)' % (np.degrees(angle), axisf)
        else:
            assert False, 'Not implemented for n>=4.'
        
                
    
