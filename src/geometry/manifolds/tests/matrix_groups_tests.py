from geometry import MatrixLieGroup
from nose.plugins.attrib import attr
from geometry.manifolds.tests.manifold_tests import manifolds_to_check


def check_matrix_group_1(M):
    for m in M.interesting_points():
        M.belongs(m)
        v = M.algebra_from_group(m)
        M.algebra.belongs(v)
        m2 = M.group_from_algebra(v)
        M.assert_close(m, m2)
        #printm('Checked %s' % M, m)


def check_matrix_group_2(M):
    algebra = M.get_algebra()
    for a in algebra.interesting_points():
        #printm('Checked %s' % M, a) 
        M.algebra.belongs(a)
        g = M.group_from_algebra(a)
        M.belongs(g)


def check_matrix_group_vector_isomorphism(M):
    algebra = M.get_algebra()
    expected = (algebra.get_dimension(),)
    for p in M.interesting_points():
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


def check_enough_points_for_algebra(M):
    algebra = M.get_algebra()
    points = list(algebra.interesting_points())
    if not points:
        raise ValueError('No test points for algebra of %s.' % M)


@attr('manifolds')
def test_group_algebra():
    ftests = [
             check_matrix_group_1,
             check_matrix_group_2,
             check_matrix_group_vector_isomorphism,
             check_enough_points_for_algebra
             ]
    for a in manifolds_to_check():
        if isinstance(a, MatrixLieGroup):
            for f in ftests:
                yield f, a
