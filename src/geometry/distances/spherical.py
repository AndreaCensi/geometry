# coding=utf-8
from contracts import contract, new_contract
# noinspection PyUnresolvedReferences
from geometry.spheres import directions  #@NoMove @UnusedImport # for contract
import numpy as np


new_contract('cosines', 'array[NxN](>=-1,<=+1)')
new_contract('angles', 'array[N](>=-pi,<=pi)')
new_contract('distances', 'array[NxN](>=0,<=pi)')


@contract(theta='array[N]', returns='array[2xN], directions')
def directions_from_angles(theta):
    """ Creates directions (elements of S1) from angles. """
    return np.vstack((np.cos(theta), np.sin(theta)))


@contract(S='array[KxN], directions', returns='array[N], angles')
def angles_from_directions(S):
    if S.shape[0] > 2:  # TODO: make contract
        assert (S[2, :] == 0).all()
    return np.arctan2(S[1, :], S[0, :])


@contract(S='array[KxN], directions', returns='array[NxN], cosines')
def cosines_from_directions(S):
    C = np.dot(S.T, S)
    return np.clip(C, -1, 1, C)


@contract(C='array[NxN], cosines', returns='array[NxN], distances')
def distances_from_cosines(C):
    return np.real(np.arccos(C))


@contract(D='distances', returns='cosines')
def cosines_from_distances(D):
    return np.cos(D)


@contract(S='directions', returns='distances')
def distances_from_directions(S):
    C = cosines_from_directions(S)
    return distances_from_cosines(C)


@contract(theta='angles', returns='distances')
def distances_from_angles(theta):
    directions = directions_from_angles(theta)
    return distances_from_directions(directions)
