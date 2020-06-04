from typing import NewType, Tuple

import numpy as np

__all__ = [
    "SO2value",
    "so2value",
    "SO3value",
    "so3value",
    "SE2value",
    "se2value",
    "TSE2value",
    "se3value",
    "SE3value",
    "TSE3value",
    "T2value",
    "T3value",
]

SO2value = NewType("SO2value", np.ndarray)
so2value = NewType("so2value", np.ndarray)

SO3value = NewType("SO3value", np.ndarray)
so3value = NewType("so3value", np.ndarray)

SE2value = NewType("SE2value", np.ndarray)
se2value = NewType("se2value", np.ndarray)
TSE2value = Tuple[SE2value, se2value]

SE3value = NewType("SE3value", np.ndarray)
se3value = NewType("se3value", np.ndarray)
TSE3value = Tuple[SE3value, se3value]

T3value = NewType("T3value", np.ndarray)  # (3,) float64 arrat
T2value = NewType("T2value", np.ndarray)  # (2,) float64 arrat
