from typing import NewType, Tuple, TYPE_CHECKING

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
    "E2value",
    "e2value",
    "E3value",
    "e3value",
    "t2value",
    "t3value",
    "V1D",
    "V1DN",
]

V1D = NewType("V1D", np.ndarray)
""" Vector 1D """
V1DN = NewType("V1DN", V1D)
""" Vector 1D normalized """

if TYPE_CHECKING:

    SO2value = NewType("SO2value", np.ndarray)
    so2value = NewType("so2value", np.ndarray)

    SO3value = NewType("SO3value", np.ndarray)
    so3value = NewType("so3value", np.ndarray)

    E2value = NewType("E2value", np.ndarray)
    e2value = NewType("e2value", np.ndarray)

    SE2value = NewType("SE2value", E2value)
    se2value = NewType("se2value", e2value)

    E3value = NewType("E3value", np.ndarray)
    e3value = NewType("e3value", np.ndarray)

    SE3value = NewType("SE3value", E3value)
    se3value = NewType("se3value", e3value)

    T3value = NewType("T3value", V1D)  # (3,) float64 arrat
    T2value = NewType("T2value", V1D)  # (2,) float64 arrat
    t3value = NewType("t3value", V1D)  # velocity
    t2value = NewType("t2value", V1D)  # velocity

else:
    SO2value = (
        so2value
    ) = (
        SO3value
    ) = (
        so3value
    ) = (
        SE2value
    ) = (
        se2value
    ) = SE3value = se3value = T3value = T2value = e3value = e2value = E3value = E2value = np.ndarray
    t3value = t2value = np.ndarray

TSE2value = Tuple[SE2value, se2value]
TSE3value = Tuple[SE3value, se3value]
