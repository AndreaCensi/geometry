from contracts import contract

from . import MatrixLieGroup, np, R, tran

from geometry import  (assert_allclose,
                       pose_from_rotation_translation,
                           rotation_translation_from_pose,
                           extract_pieces)
from geometry.poses import combine_pieces


class Tran(MatrixLieGroup):
    ''' 
        The translation subgroup of SE(n). 
    '''
    
    @contract(n='1|2|3')
    def __init__(self, n):
        algebra = tran[n]
        MatrixLieGroup.__init__(self, n + 1, algebra)
        self.En = R[n]
        
    def __repr__(self):
        return 'Tran(%s)' % (self.n - 1)
    
    def belongs_(self, x):
        R, t, zero, one = extract_pieces(x) #@UnusedVariable
        assert_allclose(R, np.eye(self.n - 1))
        assert_allclose(zero, 0, err_msg='I expect the lower row to be 0.') 
        assert_allclose(one, 1, err_msg='Bottom-right must be 1.')

    def sample_uniform(self):
        t = self.En.sample_uniform()
        return pose_from_rotation_translation(np.eye(self.n - 1), t)
            
    def friendly(self, x):
        t = rotation_translation_from_pose(x)[1]
        return 'Tran(%s)' % (self.En.friendly(t))
    
    def logmap_(self, base, target):
        return target - base
    
    def expmap_(self, base, vel):
        return base + vel

        
    def interesting_points(self):
        points = []
        for t in self.En.interesting_points():
            p = pose_from_rotation_translation(np.eye(self.n - 1), t)
            points.append(p)
                  
        return points
