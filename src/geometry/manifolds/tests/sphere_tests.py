# coding=utf-8
import numpy as np
from geometry.manifolds import S1
from geometry.utils import check_allclose
from geometry.formatting import printm


def test_wrap_around():
    a = np.array([+1, 0])
    b = np.array([-1, 0])

    bv = S1.logmap(a, b)
    b2 = S1.expmap(bv)
    d = S1.distance(b, b2)

    printm('a', a, 'b', b, 'vel', bv[1], 'd', np.array(d))
    check_allclose(d, 0, atol=1e-7)
