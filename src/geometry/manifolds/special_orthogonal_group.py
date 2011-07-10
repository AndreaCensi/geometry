from . import DifferentiableManifold, MatrixLieGroup, np, S2, so
from .. import (assert_allclose, rot2d, random_rotation, axis_angle_from_rotation,
    rotation_from_axis_angle)
from contracts import contract, check


class SO_group(MatrixLieGroup):
    ''' 
        This is the Special Orthogonal group SO(n) describing rotations
        of Euclidean space; implemented for n=2,3.
        
    '''
    
    @contract(N='int,(2|3)')
    def __init__(self, N):
        algebra = so[N]
        dimension = {2:1, 3:2}[N]
        MatrixLieGroup.__init__(self, n=N, algebra=algebra, dimension=dimension)
        DifferentiableManifold.embedding(self, algebra,
                                          self.algebra_from_group,
                                    self.group_from_algebra,
                                    type='lie')

    def __repr__(self):
        #return 'SO(%s)' % (self.n)
        return 'SO%s' % (self.n)
    
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
        
    def interesting_points(self):
        points = []
        points.append(self.identity())
        if self.n == 2:
            points.append(rot2d(np.pi))            
            points.append(rot2d(np.pi / 2))
            points.append(rot2d(-np.pi / 3))
        if self.n == 3:
            points.append(rotation_from_axis_angle(np.array([0, 0, 1]), np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([0, 0, 1]), np.pi))
            points.append(rotation_from_axis_angle(np.array([0, 1, 0]), np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([0, 1, 0]), np.pi))
            points.append(rotation_from_axis_angle(np.array([1, 0, 0]), np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([1, 0, 0]), np.pi))
    
        return points
