# coding=utf-8
from contracts import contract, describe_type
from geometry.poses import extract_pieces, pose_from_rotation_translation, \
    rotation_translation_from_pose, SE2_from_se2, se2_from_SE2, \
    SE2_from_translation_angle, SE3_from_SE2
from geometry.utils.numpy_backport import assert_allclose
import numpy as np

from .differentiable_manifold import DifferentiableManifold
from .euclidean import R
from .matrix_lie_group import MatrixLieGroup
from .special_euclidean_algebra import se
from .special_orthogonal_group import SO

__all__ = ['SE_group', 'SE', 'SE2', 'SE3', 'TSE', 'TSE2', 'TSE3']


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

    @contract(returns='array[2](>=0)')
    def distances(self, a, b):
        """ Returns linear, angular distance. """
        _, vel = self.logmap(a, b)
        W, v, _, _ = extract_pieces(vel)
        dist1 = np.linalg.norm(v)
        dist2 = self.algebra.son.norm(W)
        return np.array([dist1, dist2])

    def norm(self, X):
        W, v, zero, zero = extract_pieces(X)  # @UnusedVariable
        return np.linalg.norm(v) + self.alpha * self.son.norm(W)

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
        R, t, zero, one = extract_pieces(x)  # @UnusedVariable
        try:
            self.SOn.belongs(R)
        except:
            msg = 'The rotation is not a rotation:\n%s' % R
            raise ValueError(msg)
        assert_allclose(zero, 0, err_msg='I expect the lower row to be 0.')
        assert_allclose(one, 1)

    def sample_uniform(self):
        t = self.En.sample_uniform()
        R = self.SOn.sample_uniform()
        assert t.size == R.shape[0]
        return pose_from_rotation_translation(R, t)

    def friendly(self, a):
        R, t = rotation_translation_from_pose(a)
        return 'Pose(%s,%s)' % (self.SOn.friendly(R), self.En.friendly(t))

    # TODO: make explicit inverse
    # TODO: make specialization for SE(3)
    def group_from_algebra(self, a):
        if self.n == 3:
            return SE2_from_se2(a)
        else:
            return MatrixLieGroup.group_from_algebra(self, a)

    def algebra_from_group(self, g):
        if self.n == 3:
            return se2_from_SE2(g)
        else:
            return MatrixLieGroup.algebra_from_group(self, g)

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


SE2 = SE_group(2)
SE3 = SE_group(3)
SE = {2: SE2, 3: SE3}

TSE2 = SE2.tangent_bundle()
TSE3 = SE3.tangent_bundle()
TSE = {2: TSE2, 3: TSE3}
