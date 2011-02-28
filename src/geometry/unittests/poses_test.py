import numpy as np 

from .utils import GeoTestCase
from geometry import (translation_angle_from_SE2,
    SE2_from_translation_angle,
    se2_from_linear_angular,
    linear_angular_from_se2,
    rot2d_from_angle, angle_from_rot2d)

class RotationsTest(GeoTestCase):

    def test_conversions_SE2(self):
        def sequence():
            for i in range(4): #@UnusedVariable
                t = np.random.rand(2)
                theta = np.random.rand()
                yield t, theta
                
        self.check_conversion(sequence(),
                              SE2_from_translation_angle,
                              translation_angle_from_SE2)
    
    def test_conversions_se2(self):
        def sequence():
            for i in range(4): #@UnusedVariable
                t = np.random.rand(2)
                theta = np.random.rand()
                yield t, theta
                
        self.check_conversion(sequence(),
                              se2_from_linear_angular,
                              linear_angular_from_se2)
    
    def test_conversions_rot2d(self):
        def sequence():
            for i in range(5): #@UnusedVariable
                yield np.random.uniform(-np.pi, np.pi)
        self.check_conversion(sequence(),
                              rot2d_from_angle,
                              angle_from_rot2d)

        
