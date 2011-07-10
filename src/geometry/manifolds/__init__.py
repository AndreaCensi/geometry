import numpy as np
from contracts import contract, check, new_contract
from .. import assert_allclose

from .exceptions import DoesNotBelong

from .differentiable_manifold import DifferentiableManifold

new_contract('DifferentiableManifold', DifferentiableManifold)

from .product_manifold import ProductManifold

from .group import *
from .matrix_lie_group import *

from .sphere import Sphere, Sphere1
S1 = Sphere1()
S2 = Sphere(2)
S = {1: S1, 2: S2}

from .torus import *
T1 = Torus(1)
T2 = Torus(2)
T3 = Torus(3)
T = {1: T1, 2: T2, 3: T3}

from .euclidean import Euclidean
R1 = Euclidean(1)
R2 = Euclidean(2)
R3 = Euclidean(3)
R = {1: R1, 2: R2, 3: R3}
 
from .translation_algebra import tran
tran1 = tran(1)
tran2 = tran(2)
tran3 = tran(3)
tran = {1:tran1, 2:tran2, 3:tran3}

from .translation_group import Tran
Tran1 = Tran(1)
Tran2 = Tran(2)
Tran3 = Tran(3)
Tran = {1: Tran1, 2: Tran2, 3: Tran3}

from .special_orthogonal_algebra import so_algebra
so2 = so_algebra(2)
so3 = so_algebra(3)
so = {2:so2, 3:so3}
    
from .special_orthogonal_group import SO_group
SO2 = SO_group(2)
SO3 = SO_group(3)
SO = {2:SO2, 3:SO3}
    
from .special_euclidean_algebra import se_algebra
se2 = se_algebra(2, alpha=1)
se3 = se_algebra(3, alpha=1)
se = {2:se2, 3:se3}

from .special_euclidean_group import SE_group
SE2 = SE_group(2)
SE3 = SE_group(3)
SE = {2:SE2, 3:SE3}

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

from .embedding_relations import *
from .manifold_embedding_propagation import compute_manifold_relations
compute_manifold_relations(all_manifolds)


