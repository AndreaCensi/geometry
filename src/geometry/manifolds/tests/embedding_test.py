

from geometry.manifolds import (SO3, SO2, R1, R2, R3, SE2, SE3, S2, S1,
                                    T1, T2, T3, so2, so3, se2, se3)
from nose.plugins.attrib import attr


def  check_embed_relation(A, B):
    check_embed_relation.__dict__['description'] = 'Checking %s < %s' % (A, B)
    
    points = list(A.interesting_points())
    if not points:
        msg = 'Cannot test because manifold %s does not have interesting points' % A
        raise Exception(msg)
    for a1 in points:
        b = A.embed_in(B, a1)
        B.belongs(b)
        a2 = A.project_from(B, b)
        A.belongs(a2)
        a3 = B.project_to(A, b)
        A.belongs(a3)
        A.assert_close(a1, a2)
        A.assert_close(a1, a3)
    
@attr('embed')    
def test_embed_relations():

    yield check_embed_relation, R1, R2
    yield check_embed_relation, R2, R3
    yield check_embed_relation, R1, R3
    
    yield check_embed_relation, SO2, SO3
    yield check_embed_relation, SO2, SE3
    
    yield check_embed_relation, SO2, SE2
    yield check_embed_relation, SO3, SE3

    yield check_embed_relation, so3, se3
    yield check_embed_relation, so2, se2
    yield check_embed_relation, so2, se3
    
    yield check_embed_relation, S1, S2

    yield check_embed_relation, R1, SE2
    yield check_embed_relation, R2, SE2
    yield check_embed_relation, R1, SE3
    yield check_embed_relation, R2, SE3
    yield check_embed_relation, R3, SE3
    
    yield check_embed_relation, T1, T2
    yield check_embed_relation, T2, T3
    yield check_embed_relation, T1, T3
    
    yield check_embed_relation, T1, R1
    yield check_embed_relation, T2, R2
    yield check_embed_relation, T3, R3
    
    yield check_embed_relation, T3, SE3
    
    yield check_embed_relation, S1, SE3
    yield check_embed_relation, S2, SE3
    

