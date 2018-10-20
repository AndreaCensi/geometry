# coding=utf-8
from contracts import new_contract, contract

import numpy as np


@new_contract
@contract(D='array[NxN](>=0)')
def distance_matrix(D):
    diag = D.diagonal()
    if not np.all(diag == 0):
        msg = 'Diagonal is not zero:'
        raise ValueError(msg)
