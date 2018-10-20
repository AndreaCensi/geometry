# coding=utf-8
from geometry.manifolds import (SO3, SO2, R1, R2, R3, SE2, SE3, S2, S1, T1, T2,
    T3, so2, so3, se2, se3, Tran3, Tran2, Tran1, tran2, tran1, tran3)
from nose.plugins.attrib import attr


def check_embed_relation_cond(A, B):
    check_embed_relation_cond.description = 'Checking %s < %s' % (A, B)
    msg = None
    if not A.embeddable_in(B):
        msg = '%s is not embeddable in %s' % (A, B)
    if not B.can_represent(A):
        msg = '%s cannot represent %s' % (B, A)
    if msg:
        raise Exception('%s;\n %s: %s\n %s: %s' %
                        (msg, A, A.relations_descriptions(),
                          B, B.relations_descriptions()))


def check_embed_relation(A, B):

    check_embed_relation_cond(A, B)

    points = list(A.interesting_points())
    if not points:
        msg = ('Cannot test because manifold %s does '
               'not have interesting points' % A)
        raise Exception(msg)

    for a1 in points:
        A.belongs(a1)
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
    couples = []

    def add(A, B):
        couples.append((A, B))

    add(R1, R2)
    add(R2, R3)
    add(R1, R3)

    add(SO2, SO3)
    add(SO2, SE3)

    add(SO2, SE2)
    add(SO3, SE3)
    add(so3, se3)
    add(so2, se2)
    add(so2, se3)

    add(S1, S2)

    add(R1, SE2)
    add(R2, SE2)
    add(R1, SE3)
    add(R2, SE3)
    add(R3, SE3)
    add(Tran1, SE2)
    add(Tran2, SE2)
    add(Tran1, SE3)
    add(Tran2, SE3)
    add(Tran3, SE3)

    add(T1, T2)
    add(T2, T3)
    add(T1, T3)

    add(T1, R1)
    add(T2, R2)
    add(T3, R3)

    add(T3, SE3)

    add(S1, SE3)
    add(S2, SE3)

    add(tran1, se3)
    add(tran2, se3)
    add(tran3, se3)

    add(T1, S1)

    for A, B in couples:
        check_embed_relation(A, B)
