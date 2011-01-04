from .common_imports import *

@contracts(theta='number', returns='rotation_matrix')
def rotz(theta):
    ''' Returns a 3x3 rotation matrix corresponding to rotation around the z axis. '''
    return array([ 
            [ cos(theta), -sin(theta), 0],
            [ sin(theta), cos(theta), 0],
            [0, 0, 1]]) 


def rot2d(theta):
    ''' Returns a 2x2 rotation matrix. '''
    return array([ 
            [ cos(theta), -sin(theta)],
            [ sin(theta), cos(theta)]]) 

