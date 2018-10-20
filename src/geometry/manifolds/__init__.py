# coding=utf-8
from contracts import new_contract

from .differentiable_manifold import *
from .embedding_relations import *
from .euclidean import *
from .exceptions import *
from .group import *
from .manifold_embedding_propagation import *
from .matrix_lie_algebra import *
from .matrix_lie_group import *
from .matrix_lie_group_tangent import *
from .matrix_linear_space import *
from .point_set import *
from .product_manifold import *
from .special_euclidean_algebra import *
from .special_euclidean_group import *
from .special_euclidean_group import *
from .special_orthogonal_algebra import *
from .special_orthogonal_group import *
from .sphere import *
from .square import *
from .tangent_bundle import *
from .torus import *
from .torus01 import *
from .translation_algebra import *
from .translation_group import *

new_contract('DifferentiableManifold', DifferentiableManifold)

# keep at the end   #@NoMove

all_manifolds = [
    SO3, SO2,
    R1, R2, R3,
    T1, T2, T3,
    Tran1, Tran2, Tran3,
    SE2, SE3,
    S1, S2,
    se2, se3,
    so2, so3,
    tran1, tran2, tran3,
    TSE2, TSE3,
    Ts1, Ts2, Ts3,
    Sq1, Sq2, Sq3
]

compute_manifold_relations(all_manifolds)
