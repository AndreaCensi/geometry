# coding=utf-8
import itertools

from contracts.utils import raise_wrapped
from nose.tools import nottest

from geometry import MatrixLieGroup, RandomManifold, all_manifolds, logger
from .checks_generation import *


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
            point = interesting[i]
            try:
                M.belongs(point)
            except Exception as e:
                msg = 'M %s does not contain %s: %s' % (M, point, e)
                raise_wrapped(Exception, e, msg)

            yield M, point, i, num_examples


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
            point = interesting[i]
            try:
                M.belongs(point)
            except Exception as e:
                msg = 'M %s does not contain %s: %s' % (M, point, e)
                raise_wrapped(Exception, e, msg)
            yield M, point, i, num_examples


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


def _args0(x):
    (M, p, i, n) = x
    return M, p


def _attrs0(x):
    (M, p, i, n) = x
    return dict(manifolds=1,
                manifold=M,
                point=p)


for_all_manifold_point = fancy_test_decorator(lister=list_manifold_point,
                                              arguments=_args0,
                                              attributes=_attrs0)


def _args1(x):
    (M, p, i, n) = x
    return M, p


def _attrs1(x):
    (M, p, i, n) = x
    return dict(manifolds=1,
                matrixgroups=1,
                manifold=M, point=p)


for_all_mgroup_point = fancy_test_decorator(lister=list_mgroup_point,
                                            arguments=_args1,
                                            attributes=_attrs1)

for_all_mgroup = fancy_test_decorator(lister=list_mgroup,
                                      arguments=lambda M: (M,),
                                      attributes=lambda M: dict(manifolds=1, matrixgroups=1,
                                                                manifold=M))


def _args(x):
    (M, p1, p2, k, n) = x
    return M, p1, p2


def _attrs(x):
    (M, p1, p2, k, n) = x
    return dict(type='manifolds', manifold=M, point1=p1, point2=p2)


for_all_manifold_pairs = fancy_test_decorator(lister=list_manifold_points,
                                              arguments=_args,
                                              attributes=_attrs)
