# coding=utf-8
from nose.plugins.attrib import attr

from geometry import (random_direction, random_directions_bounded,
    distances_from, spherical_cap_area, spherical_cap_with_area)
import numpy as np

try:
    from stochastic_testing import (DiscreteUniformDistribution,
                                    StochasticTestManager, stochastic)

except ImportError:
    print('Warning: skipping stochastic testing,'
          ' because package "stochastic_testing" not installed.')

else:
    def random_directions_bounded_density_3d(center, radius, N):

        S = random_directions_bounded(3, radius, N, center=center)
        distances = distances_from(S, center)

        if not (distances <= radius).all():
            invalid = np.nonzero(distances > radius)[0]
            msg = 'Invalid distances: %s > %f' % (distances[invalid], radius)
            raise Exception(msg)

        subs = 6
        A = spherical_cap_area(cap_radius=radius)
        da = A / subs
        dist = np.zeros(subs, dtype='int')
        for s in range(subs):
            lower = s * da
            upper = lower + da

            r1 = spherical_cap_with_area(lower)
            r2 = spherical_cap_with_area(upper)
            num_here = np.logical_and(distances >= r1, distances < r2).sum()

            dist[s] = num_here

        assert dist.sum() == N
        return DiscreteUniformDistribution(dist,
                                    'Distribution of distances from center')

    @stochastic
    def random_directions_bounded_density_test():
        radius = [np.pi, np.pi * 3 / 4, np.pi / 2, np.pi / 4, np.pi / 6]
        N = 100
        for r in radius:
            center = random_direction()
            yield random_directions_bounded_density_3d, center, r, N

    def random_orthogonal_direction_density_test():
        # TODO
        pass

    @attr('density')
    def test_stochastic():
        StochasticTestManager.main.run(time_limit=10)

    if __name__ == '__main__':
        random_directions_bounded_density_test()
        random_orthogonal_direction_density_test()
