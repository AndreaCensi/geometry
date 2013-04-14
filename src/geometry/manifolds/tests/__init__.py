from .. import np, logger

from .checks_generation import *
from geometry.manifolds import all_manifolds
import itertools
from geometry.manifolds.differentiable_manifold import RandomManifold
from geometry.manifolds.matrix_lie_group import MatrixLieGroup
from nose.tools import nottest


def list_manifolds():
    return all_manifolds


@nottest
def get_test_points(M, num_random=2):
    interesting = M.interesting_points()
    if isinstance(M, RandomManifold):
        for i in range(num_random):  # @UnusedVariable
            interesting.append(M.sample_uniform())
            
    if len(interesting) == 0:
        logger.warning('No test points for %s and not random.' % M)
    return interesting


def list_manifold_point():
    """ Yields all possible (M, point, i, num) tests we have """
    for M in list_manifolds():
        interesting = get_test_points(M)
        num_examples = len(interesting)
        for i in range(num_examples):
            yield M, interesting[i], i, num_examples
            

def list_mgroup():
    """ Yields all possible (M, point, i, num) tests we have """
    for M in list_manifolds():
        if not isinstance(M, MatrixLieGroup):
            continue
        yield M

def list_mgroup_point():
    """ Yields all possible (M, point, i, num) tests we have """
    for M in list_mgroup():
        interesting = get_test_points(M)
        num_examples = len(interesting)
        for i in range(num_examples):
            yield M, interesting[i], i, num_examples
            
def list_manifold_points():
    """ Yields all possible (M, point1, point2, i, num) tests we have """
    for M in list_manifolds():
        interesting = get_test_points(M)
        num_examples = len(interesting) * len(interesting)
        k = 0
        for p1, p2 in itertools.product(interesting, interesting):
            yield M, p1, p2, k, num_examples
            k += 1
            
for_all_manifolds = fancy_test_decorator(lister=lambda: all_manifolds,
            arguments=lambda M: (M,),
            attributes=lambda M: dict(manifolds=1, manifold=str(M)))


for_all_manifold_point = fancy_test_decorator(lister=list_manifold_point,
            arguments=lambda (M, p, i, n): (M, p),  # @UnusedVariable
            attributes=lambda (M, p, i, n): dict(manifolds=1,  # @UnusedVariable
                                               manifold=M, point=p))  # @UnusedVariable


for_all_mgroup_point = fancy_test_decorator(lister=list_mgroup_point,
            arguments=lambda (M, p, i, n): (M, p),  # @UnusedVariable
            attributes=lambda (M, p, i, n): dict(manifolds=1,  # @UnusedVariable
                                                 matrixgroups=1,
                                                 manifold=M, point=p)) 

for_all_mgroup = fancy_test_decorator(lister=list_mgroup,
            arguments=lambda M: (M,),
            attributes=lambda M: dict(manifolds=1, matrixgroups=1,
                                                 manifold=M)) 

for_all_manifold_pairs = fancy_test_decorator(lister=list_manifold_points,
            arguments=lambda (M, p1, p2, k, n): (M, p1, p2),  # @UnusedVariable
            attributes=lambda (M, p1, p2, k, n): dict(type='manifolds', manifold=M, point1=p1, point2=p2))  # @UnusedVariable
