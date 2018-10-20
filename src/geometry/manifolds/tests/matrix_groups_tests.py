# coding=utf-8
from . import for_all_mgroup_point, for_all_mgroup


@for_all_mgroup_point
def algebra1(M, m):
    M.belongs(m)
    v = M.algebra_from_group(m)
    M.algebra.belongs(v)
    m2 = M.group_from_algebra(v)
    M.assert_close(m, m2)


@for_all_mgroup
def algebra2(M):
    algebra = M.get_algebra()
    for a in algebra.interesting_points():
        #printm('Checked %s' % M, a)
        M.algebra.belongs(a)
        g = M.group_from_algebra(a)
        M.belongs(g)


@for_all_mgroup_point
def group_vector_isomorphism(M, p):
    algebra = M.get_algebra()
    expected = (algebra.get_dimension(),)

    M.belongs(p)
    # convert point to algebra
    a = M.algebra_from_group(p)
    algebra.belongs(a)
    # convert algebra to vector
    v = algebra.vector_from_algebra(a)

    if v.shape != expected:
        raise ValueError('%s: expected %s, got %s ' %
                         (algebra, expected, v.shape))

    # Now back to algebra
    a2 = algebra.algebra_from_vector(v)
    algebra.belongs(a2)
    algebra.assert_close(a, a2)


@for_all_mgroup
def algebra_enough(M):
    algebra = M.get_algebra()
    points = list(algebra.interesting_points())
    if not points:
        raise ValueError('No test points for algebra of %s.' % M)

