from .common_imports import *
from .geometry_contracts import deprecated

# TodO: convert
#def so3_geodesic(r, r0):
#    r_mat = mat(r).T
#    r0_mat = mat(r0).T
#    return abs(myacos((trace(r0_mat.T * r_mat)-1)/2))

@deprecated
@contracts(s='direction', v='direction', returns='float,>=0,<=3.1416')
def geodesic_distance_on_S2(s, v):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s == v).all(): return 0.0
    dot_product = np.clip((s * v).sum(), -1, 1) # safe to clip if directions
    return np.arccos(dot_product) # safe to arccos() if clipped

@contracts(s='array[K],unit_length',
           v='array[K],unit_length', returns='float,>=0,<=3.1416')
def geodesic_distance_on_sphere(s, v):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s == v).all(): return 0.0
    dot_product = np.clip((s * v).sum(), -1, 1) # safe to clip if directions
    return np.arccos(dot_product) # safe to arccos() if clipped

