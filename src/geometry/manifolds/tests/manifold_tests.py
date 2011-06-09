from nose.plugins.attrib import attr
import numpy as np
import itertools

from geometry import assert_allclose
from geometry.manifolds import (SO3, SO2, E1, E2, SE2, SE3, S2, S1,
                                    T1, T2, T3)


def check_geodesic_consistency(M, a, b, divisions=5):
    check_geodesic_consistency.description = (
        '%s: Checking geodesic consistency. '
        '(a: %s, b: %s)' 
        % (M, M.friendly(a), M.friendly(b)))
    
    ''' Check that there is consistency in the geodesics. '''
    d = M.distance(a, b)
    
    ts = np.linspace(0, 1, divisions)
    for t in ts:
        c = M.geodesic(a, b, t)
        M.belongs(c)
        d1 = M.distance(a, c)
        d2 = M.distance(c, b)
        
        assert_allclose(d1 + d2, d, atol=1e-7)

def check_logmap1(M, a, b):
    check_logmap1.description = (
        '%s: Checking that logmap/expmap work. '
        '(a: %s, b: %s)' 
        % (M, M.friendly(a), M.friendly(b)))
    
    vel = M.logmap(a, b)
    b2 = M.expmap(a, vel)
    assert_allclose(M.distance(b, b2), 0, atol=1e-7)

def check_logmap2(M, a, b):
    vel1 = M.logmap(a, b)
    vel2 = M.logmap(b, a)
    # TODO: use parallel transport

def check_logmap3(M, a, b):
    check_logmap3.description = (
        '%s: Checking that distance is consistent with logmap/expmap '
        '(a: %s, b: %s)' 
        % (M, M.friendly(a), M.friendly(b)))

    d = M.distance(a, b)
    vel = M.logmap(a, b)
    ratios = [0.5, 0.3]
    for ratio in ratios:
        b2 = M.expmap(a, vel * ratio)
        d2 = M.distance(a, b2)
        assert_allclose(d * ratio, d2, atol=1e-7)

def check_friendly(M, a):
    print('Friendly: %s %s ' % (M, a))
    
def check_manifold_suite(M, num_random=5): 

    points = M.interesting_points()
    for i in range(num_random): #@UnusedVariable
        points.append(M.sample_uniform())
    
    for p in points:
        M.belongs(p)
    
    for f in [check_friendly]:
        for a in points:
            yield f, M, a

    for f in [check_geodesic_consistency,
              check_logmap1, check_logmap3]:
        for a, b in itertools.product(points, points):
            yield f, M, a, b


def get_manifolds():
    M = []
    M += [E1]
    M += [E2]
    M += [S1]
    M += [S2]
    M += [ SO2 ]
    M += [ SO3 ]
    M += [ SE2 ]
    M += [ SE3 ]
    M += [T1]
    M += [T2]
    M += [T3]
    return M

@attr('manifolds')
def test_manifolds():
    for M in get_manifolds():
        for x in check_manifold_suite(M): yield x


if __name__ == '__main__':
    test_manifolds()
     
