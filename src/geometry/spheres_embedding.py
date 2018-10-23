# coding=utf-8
from contracts import contract
import numpy as np


@contract(returns='S2', a='S1')
def S2_from_S1(a):
    return np.array([a[0], a[1], 0])


@contract(returns='S1', b='S2')
def S1_project_from_S2(b):
    if np.abs(b[2]) == 1:
        return np.array([1, 0])
    theta = np.arctan2(b[1], b[0])
    return np.array([np.cos(theta), np.sin(theta)])


@contract(returns='S1', b='R2')
def S1_project_from_R2(b):
    norm = np.linalg.norm(b)
    atol = 1e-8  # XXX
    if norm <= atol:
        return np.array([1, 0])
    return b / norm


@contract(returns='S2', b='R3')
def S2_project_from_R3(b):
    norm = np.linalg.norm(b)
    atol = 1e-8  # XXX
    if norm <= atol:
        return np.array([1, 0, 0])
    return b / norm

