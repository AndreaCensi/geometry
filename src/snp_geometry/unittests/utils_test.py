from snp_geometry import (sphere_area, spherical_cap_area, assert_allclose, pi,
                          spherical_cap_with_area)

A = sphere_area()

couples = [(0, 0), (pi / 2, A / 2), (pi, A) ]

    
def spherical_cap_area_test():    
    for radius, area in couples:
        yield  assert_allclose, spherical_cap_area(radius), area        

def spherical_cap_with_area_test():    
    for radius, area in couples:
        yield  assert_allclose, spherical_cap_with_area(area), radius
