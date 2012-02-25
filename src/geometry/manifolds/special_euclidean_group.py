from . import DifferentiableManifold, MatrixLieGroup, SO, se, R, contract, np
from .. import (SE3_from_SE2, assert_allclose, pose_from_rotation_translation,
    rotation_translation_from_pose, extract_pieces, se2_from_SE2, SE2_from_se2,
    SE2_from_translation_angle)
from contracts import describe_type


class SE_group(MatrixLieGroup):
    ''' 
        This is the Special Euclidean group SE(n) 
        describing roto-translations of Euclidean space.
        Implemented only for n=2,3.
        
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''

    @contract(N='int,(2|3)')
    def __init__(self, N):
        algebra = se[N]
        self.SOn = SO[N]
        self.En = R[N]
        dimension = {2: 3, 3: 6}[N]
        MatrixLieGroup.__init__(self, n=N + 1,
                                algebra=algebra, dimension=dimension)

        DifferentiableManifold.embedding(self,
                                         algebra,
                                         self.algebra_from_group,
                                         self.group_from_algebra,
                                         itype='lie')

    def __repr__(self):
        return 'SE%s' % (self.n - 1)

    @contract(x='array[NxN]')
    def belongs(self, x):
        # TODO: more checks
        if not isinstance(x, np.ndarray):
            msg = 'Expected a numpy array (%s)' % describe_type(x)
            raise ValueError(msg)
        if not x.shape == (self.n, self.n):
            msg = ('Expected shape %dx%d instead of (%s)' %
                    (self.n, self.n, x.shape))
            raise ValueError(msg)
        R, t, zero, one = extract_pieces(x) #@UnusedVariable
        self.SOn.belongs(R)
        assert_allclose(zero, 0, err_msg='I expect the lower row to be 0.')
        assert_allclose(one, 1)

    def sample_uniform(self):
        t = self.En.sample_uniform()
        R = self.SOn.sample_uniform()
        assert t.size == R.shape[0]
        return pose_from_rotation_translation(R, t)

    def friendly(self, x):
        R, t = rotation_translation_from_pose(x)
        return 'Pose(%s,%s)' % (self.SOn.friendly(R), self.En.friendly(t))

    # TODO: make explicit inverse
    # TODO: make specialization for SE(3)
    def group_from_algebra(self, g):
        if self.n == 3:
            return SE2_from_se2(g)
        else:
            return MatrixLieGroup.group_from_algebra(self, g)

    def algebra_from_group(self, a):
        if self.n == 3:
            return se2_from_SE2(a)
        else:
            return MatrixLieGroup.algebra_from_group(self, a)

    def interesting_points(self):
        if self.n == 3:
            return [
                SE2_from_translation_angle([0, 0], 0),
                SE2_from_translation_angle([0, 0], 0.1),
                SE2_from_translation_angle([0, 0], -0.1),
                SE2_from_translation_angle([1, 0.1], 0),
            ]
        elif self.n == 4:
            # TODO: better implementation
            return [
                SE3_from_SE2(SE2_from_translation_angle([0, 0], 0)),
                SE3_from_SE2(SE2_from_translation_angle([0, 0], 0.1)),
                SE3_from_SE2(SE2_from_translation_angle([0, 0], -0.1)),
                SE3_from_SE2(SE2_from_translation_angle([1, 0.1], 0)),
            ]
        else:
            assert False


