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


@contracts(S='directions', returns='float,>=0,<=3.1416')
def distribution_radius(S):
    ''' Returns the radius of the given directions distribution.
        The radius is defined as the minimum R such that there exists a C
        such that all distances are within R from C. ::
        
            R = min { R | there is a C such that d(C,x) <= R for all x in S }
    '''
    D = np.arccos(np.clip(dot(S.T, S), -1, 1))
    distances = D.max(axis=0)
    center = np.argmin(distances) 
    return distances[center]


def normalize_length(s, norm=2):
    ''' Normalize an array such that it has unit length in the given norm. '''
    sn = np.linalg.norm(s, norm)
    if sn == 0: # TODO: add tolerance
        return s
    else:
        return s / sn
    

@contracts(S='array[3xK],directions', axis='direction',
           returns='array[K](>=0,<=3.15)')
def distances_from(S, axis):
    ''' Returns the distances of S from the given axis. '''
    return np.arccos(np.clip(np.dot(axis, S), -1, 1))
    
