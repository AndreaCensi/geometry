from nose.plugins.attrib import attr
from geometry.manifolds import all_manifolds
from geometry.manifolds.matrix_lie_group import MatrixLieGroup
from geometry.formatting import printm

def check_matrix_group(M):
    
    for m in M.interesting_points(): 
        M.belongs(m)
        v = M.algebra_from_group(m)
        M.algebra.belongs(v)
        m2 = M.group_from_algebra(v)
        M.assert_close(m, m2)
        #printm('Checked %s' % M, m)

    for a in M.algebra.interesting_points():
        #printm('Checked %s' % M, a) 
        M.algebra.belongs(a)
        g = M.group_from_algebra(a)
        M.belongs(g)


@attr('lie')
def test_group_algebra():
    for a in all_manifolds:
        if isinstance(a, MatrixLieGroup):
            yield check_matrix_group, a
