from .common_imports import *

@contracts(theta='number', returns='rotation_matrix')
def rotz(theta):
    ''' Returns a 3x3 rotation matrix corresponding to rotation around the z axis. '''
    return array([ 
            [ cos(theta), -sin(theta), 0],
            [ sin(theta), cos(theta), 0],
            [0, 0, 1]]) 

@contracts(theta='number')
def rot2d(theta):
    ''' Returns a 2x2 rotation matrix. '''
    return array([ 
            [ cos(theta), -sin(theta)],
            [ sin(theta), cos(theta)]]) 

def sphere_area(r=1):
    ''' Returns the area of a sphere of the given radius. ''' 
    return 4 * pi * (r ** 2)

def spherical_cap_area(cap_radius):
    ''' Returns the area of a spherical cap on the unit sphere 
        of the given radius. 
    
        See figure at http://mathworld.wolfram.com/SphericalCap.html
    '''
    h = 1 - np.cos(cap_radius)
    a = np.sin(cap_radius)
    A = np.pi * (a ** 2 + h ** 2)
    return A

def spherical_cap_with_area(cap_area):
    ''' Returns the radius of a spherical cap of the given area. '''
    # http://www.springerlink.com/content/3521h167300g7v62/
    A = cap_area
    L = np.sqrt(A / pi)
    h = L ** 2 / 2
    r = np.arccos(1 - h)
    return r


