import numpy as np
from snp_geometry import random_direction, random_directions_bounded, distances_from
from snp_geometry.utils import spherical_cap_area, spherical_cap_with_area
from nose.plugins.attrib import attr
from scipy.stats.stats import chisqprob
from nose.tools import nottest

def uniform_dist_pvalue(dist):
    # http://en.wikipedia.org/wiki/Pearson's_chi-square_test#Discrete_uniform_distribution
    Ei = dist.sum() / dist.size
    Oi = dist
    chi2 = ((Ei - Oi) ** 2 / Ei).sum()
    pvalue = chisqprob(chi2, dist.size - 1) 
    return pvalue 
        
class TestStatistic(object):
    def pvalue(self):
        assert False

class DiscreteUniformDistribution(TestStatistic):
    def __init__(self, dist, desc='Uniform distribution'):
        assert dist.dtype == 'int'
        self.dist = dist
        self.desc = desc

    def pvalue(self):
        return uniform_dist_pvalue(self.dist)
    
    def __str__(self):
        pval = self.pvalue()
        return '%s: %s pvalue %.5f' % (self.desc, self.dist, pval)

@nottest
def statistical_test(f):
    ''' The function f should return a TestStatistic object. '''
    # TODO: add another level of tests
    def stat_wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        assert isinstance(result, TestStatistic), type(result)
        # TODO: multiple
        pvalue = result.pvalue()
        sig = 0.05
        msg = ('Test statistic for function %s gave %.5f significance.\n' % 
               (f.__name__, pvalue))
        msg += '- statistics: %s' % result
        if pvalue < sig:
            raise Exception(msg)
        else:
            print msg 
    return stat_wrapper
        
        
@statistical_test
def random_directions_bounded_density_check_3d(center, radius, N):
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
    return DiscreteUniformDistribution(dist, 'Distribution of distances from center')
    
@attr('density')
def random_directions_bounded_density_test():
    radius = [np.pi, np.pi * 3 / 4, np.pi / 2, np.pi / 4, np.pi / 6]
    N = 100
    for r in radius:
        center = random_direction()
        yield random_directions_bounded_density_check_3d, center, r, N
    
    
    
def random_orthogonal_direction_density_test():
    # TODO
    pass

    
if __name__ == '__main__':
    random_directions_bounded_density_test()
    random_orthogonal_direction_density_test()
