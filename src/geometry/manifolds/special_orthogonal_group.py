# coding=utf-8
import numpy as np
from contracts import check, contract

from geometry.rotations import rot2d, random_rotation, axis_angle_from_rotation, \
    rotation_from_axis_angle
from geometry.utils import assert_allclose
from .differentiable_manifold import DifferentiableManifold
from .matrix_lie_group import MatrixLieGroup
from .special_orthogonal_algebra import so
from .sphere import S2

__all__ = ['SO_group', 'SO', 'SO2', 'SO3']


class SO_group(MatrixLieGroup):
    '''
        This is the Special Orthogonal group SO(n) describing rotations
        of Euclidean space; implemented for n=2,3.

        TODO: do SO2 and SO3 separately
    '''

    @contract(N='int,(2|3)')
    def __init__(self, N):
        algebra = so[N]
        dimension = {2: 1, 3: 3}[N]
        MatrixLieGroup.__init__(self, n=N, algebra=algebra,
                                dimension=dimension)
        DifferentiableManifold.embedding(self, algebra,
                                         self.algebra_from_group,
                                         self.group_from_algebra,
                                         itype='lie')

    def __repr__(self):
        return 'SO%s' % self.n

    def belongs(self, x):
        # TODO: make this much more efficient
        check('array[NxN],orthogonal', x, N=self.n)
        det = np.linalg.det(x)
        assert_allclose(det, 1, err_msg='I expect the determinant to be +1.')

    @contract(returns='belongs')
    def sample_uniform(self):
        if self.n == 2:
            theta = np.random.rand() * np.pi
            return rot2d(theta)
        elif self.n == 3:
            return random_rotation()
        else:
            assert False, 'Not implemented for n>=4.'

    def friendly(self, a):
        if self.n == 2:
            theta = np.arctan2(a[1, 0], a[0, 0])
            return 'Rot(%.1fdeg)' % np.degrees(theta)
        elif self.n == 3:
            axis, angle = axis_angle_from_rotation(a)
            axisf = S2.friendly(axis)
            return 'Rot(%.1fdeg, %s)' % (float(np.degrees(angle)), axisf)
        else:
            raise ValueError('Not implemented for n>=4.')

    @contract(returns='list(belongs)')
    def interesting_points(self):
        points = []
        points.append(self.identity())
        if self.n == 2:
            points.append(rot2d(np.pi))
            points.append(rot2d(np.pi / 2))
            points.append(rot2d(-np.pi / 3))
        if self.n == 3:
            points.append(rotation_from_axis_angle(np.array([0, 0, 1]),
                                                   np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([0, 0, 1]), np.pi))
            points.append(rotation_from_axis_angle(np.array([0, 1, 0]),
                                                   np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([0, 1, 0]), np.pi))
            points.append(rotation_from_axis_angle(np.array([1, 0, 0]),
                                                   np.pi / 2))
            points.append(rotation_from_axis_angle(np.array([1, 0, 0]), np.pi))

        return points


SO2 = SO_group(2)
SO3 = SO_group(3)
SO = {2: SO2, 3: SO3}
