from .common_imports import *
from .rotations import axis_angle_from_rotation, safe_arccos

@contracts(R0='rotation_matrix', R1='rotation_matrix', returns='float,>=0,<=3.15')
def geodesic_distance_for_rotations(R0, R1):
    R = dot(R0, R1.T)
    axis1, angle1 = axis_angle_from_rotation(R) #@UnusedVariable
    return angle1 


@contracts(s='array[K],unit_length',
           v='array[K],unit_length', returns='float,>=0,<=3.1416')
def geodesic_distance_on_sphere(s, v):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s == v).all(): return 0.0
    dot_product = (s * v).sum()
    return safe_arccos(dot_product)


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

@contracts(s='array')
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
    
