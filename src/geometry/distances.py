from .common_imports import *
from .rotations import axis_angle_from_rotation, safe_arccos

@contract(R1='rotation_matrix', R2='rotation_matrix', returns='float,>=0,<=pi')
def geodesic_distance_for_rotations(R1, R2):
    ''' 
        Returns the geodesic distance between two rotation matrices.
        
        It is computed as the angle of the rotation :math:`R_1^{*} R_2^{-1}``.
    
    '''
    R = dot(R1, R2.T)
    axis1, angle1 = axis_angle_from_rotation(R) #@UnusedVariable
    return angle1 


@contract(s1='array[K],unit_length',
           s2='array[K],unit_length', returns='float,>=0,<=pi')
def geodesic_distance_on_sphere(s1, s2):
    ''' Returns the geodesic distance between two points on the sphere. '''
    # special case: return a 0 (no precision issues) if the vectors are the same
    if (s1 == s2).all(): return 0.0
    dot_product = (s1 * s2).sum()
    return safe_arccos(dot_product)


@contract(S='directions', returns='float,>=0,<=pi')
def distribution_radius(S):
    ''' Returns the radius of the given directions distribution.
        
        The radius is defined as the minimum *r* such that there exists a 
        point *s* in *S* such that all distances are within *r* from *s*. 
        
        .. math:: \\textsf{radius} = \\min \\{ r | \\exists s :  \\forall x \\in S : d(s,x) <= r \\}
    '''
    D = np.arccos(np.clip(dot(S.T, S), -1, 1))
    distances = D.max(axis=0)
    center = np.argmin(distances) 
    return distances[center]

@contract(s='array')
def normalize_length(s, norm=2):
    ''' Normalize an array such that it has unit length in the given norm. '''
    sn = np.linalg.norm(s, norm)
    if sn == 0: # TODO: add tolerance
        raise ValueError('Norm is zero')
    else:
        return s / sn

@contract(s='array')
def normalize_length_or_zero(s, norm=2):
    ''' 
        Normalize an array such that it has unit length in the given norm; if the
        norm is close to zero, the zero vector is returned.     
    '''
    sn = np.linalg.norm(s, norm)
    if sn == 0: # TODO: add tolerance
        return s
    else:
        return s / sn

@contract(S='array[3xK],directions', s='direction',
           returns='array[K](>=0,<=pi)')
def distances_from(S, s):
    ''' 
        Returns the geodesic distances on the sphere from a set of
        points *S* to a given point *s*. 
        
    '''
    return np.arccos(np.clip(np.dot(s, S), -1, 1))
    
