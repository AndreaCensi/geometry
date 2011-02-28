import numpy as np
from contracts import contract, check
from geometry import assert_allclose

from .base import *
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

