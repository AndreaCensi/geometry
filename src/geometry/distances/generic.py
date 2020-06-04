# coding=utf-8
import numpy as np
from contracts import new_contract, contract

__all__ = [
    "distance_matrix",
]


@new_contract
@contract(D="array[NxN](>=0)")
def distance_matrix(D):
    diag = D.diagonal()
    if not np.all(diag == 0):
        msg = "Diagonal is not zero:"
        raise ValueError(msg)
