import numpy as np
from contracts import contract, check, new_contract
from geometry import assert_allclose

from .exceptions import DoesNotBelong

from .differentiable_manifold import DifferentiableManifold
new_contract('DifferentiableManifold', DifferentiableManifold)

from .product_manifold import ProductManifold

from .group import *
from .matrix_lie_group import *

from .sphere import Sphere

S1 = Sphere(1)
S2 = Sphere(2)

from .torus import *


T1 = Torus(1)
T2 = Torus(2)
T3 = Torus(3)

from .moebius import *

from .euclidean import Euclidean
E1 = Euclidean(1)
E2 = Euclidean(2)
E3 = Euclidean(3)
R1 = E1
R2 = E2
R3 = Euclidean(3)


from .translation_matrix_group import Tran, tran 
Tran1 = Tran(1)
Tran2 = Tran(2)
Tran3 = Tran(3)
tran1 = tran(1)
tran2 = tran(2)
tran3 = tran(3)

from .special_orthogonal import SO, so

#: 3D rotations
SO3 = SO(3)
#: 2D rotations
SO2 = SO(2)
so3 = so(3)
so2 = so(2)

from .special_euclidean import SE, se
SE3 = SE(3)
SE2 = SE(2)
se3 = se(3, alpha=1)
se2 = se(2, alpha=1)

from . import embedding_relations

all_manifolds = [ 
    SO3, SO2,
    R1, R2, R3,
    T1, T2, T3,
    Tran1, Tran2, Tran3,
    tran1, tran2, tran3,
    SE2, SE3,
    S1, S2,
    se2, se3,
    so2, so3,
]
