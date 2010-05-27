from numpy import cos, sin, array

def rotz(theta):
    return array([ 
            [ cos(theta), -sin(theta), 0],
            [ sin(theta), cos(theta), 0],
            [0, 0, 1]]) 
