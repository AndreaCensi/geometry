from nose.plugins.attrib import attr
import numpy as np
import itertools

from geometry import assert_allclose
from geometry.manifolds import all_manifolds
from geometry.manifolds.differentiable_manifold import RandomManifold

def check_geodesic_consistency(M, a, b, divisions=5):
    ''' 
        Check that there is consistency in the geodesics. 
    
        This is a test that 
        
            x(t) = geodesic( a, b, t) 
            
        interpolates between a and b, checking 
            
            d(a, x(t)) + d(x(t), b) = d(a,b)
    
    '''
    check_geodesic_consistency.description = (
        '%s: Checking geodesic consistency. '
        '(a: %s, b: %s)' 
        % (M, M.friendly(a), M.friendly(b)))
    
    d = M.distance(a, b)
    
    ts = np.linspace(0, 1, divisions)
    for t in ts:
        c = M.geodesic(a, b, t)
        M.belongs(c)
        d1 = M.distance(a, c)
        d2 = M.distance(c, b)
        
        assert_allclose(d1 + d2, d, atol=1e-7)

def check_logmap1(M, a, b):
    ''' This is a test that:
    
            Exp_a( Log_a(b) ) = b
            
    '''
    check_logmap1.description = (
        '%s: Checking that logmap/expmap work. '
        '(a: %s, b: %s)' 
        % (M, M.friendly(a), M.friendly(b)))
    
    vel = M.logmap(a, b)
    b2 = M.expmap(a, vel)
    assert_allclose(M.distance(b, b2), 0, atol=1e-7)
 

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
    M.friendly(a)


def check_interesting_point_in_manifold(M, p):    
    check_interesting_point_in_manifold.description = '%s: %s' % (M, p)
    M.belongs(p, msg='Interesting point not in manifold.')
        
def check_manifold_suite(M, num_random=5): 

    points = M.interesting_points()
    
    if isinstance(M, RandomManifold):
        for i in range(num_random): #@UnusedVariable
            points.append(M.sample_uniform())
    
    for p in points:
        yield check_interesting_point_in_manifold, M, p
    
    for f in [check_friendly]:
        for a in points:
            yield f, M, a

    for f in [check_geodesic_consistency,
              check_logmap1, check_logmap3
              ]:
        for a, b in itertools.product(points, points):
            yield f, M, a, b



@attr('manifolds')
def test_manifolds():
    for M in all_manifolds:
        for x in check_manifold_suite(M): yield x


if __name__ == '__main__':
    test_manifolds()
     
