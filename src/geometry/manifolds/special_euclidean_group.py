from . import DifferentiableManifold, MatrixLieGroup, np, SO, se, R
from .. import (assert_allclose, pose_from_rotation_translation,
    rotation_translation_from_pose, extract_pieces, se2_from_SE2, SE2_from_se2,
    SE2_from_translation_angle, SE2_from_xytheta)
from contracts import contract, describe_value
from geometry.poses import SE3_from_SE2


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
#        print('Instantiating SE%s' % N)
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
        assert x.shape == (self.n, self.n)
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

    # FIXME: this old interface must be removed
    def from_yaml(self, value):
        ''' Parses from yaml value. '''
        if self.n == 3: # SE2
            x = np.array(value)
            if x.shape != (3,):
                msg = 'I expect a 3-array, not %s' % describe_value(value)
                raise ValueError(msg)
            return SE2_from_xytheta(x)
        else:
            raise ValueError('Not implemented in %r' % self.__class__.__name__)



