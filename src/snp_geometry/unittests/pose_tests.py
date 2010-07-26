from snp_geometry import Pose
import unittest
from numpy import random, pi, array, ndarray
from numpy.testing import assert_almost_equal
import numpy

class CompositionTests(unittest.TestCase):
    
    def getRandom(self):
        return Pose(position=random.randn(2), attitude=random.rand(1) * pi)
        
    def testInterface(self):
        """ Testing some basic facts """
        self.assertEqual(Pose(), Pose())
        self.assertRaises(TypeError, Pose().__eq__, None)
        self.assertRaises(TypeError, Pose().__eq__, 42)
        self.assertRaises(TypeError, Pose().oplus, None)
        self.assertRaises(TypeError, Pose().oplus, 42)
  
    def testInitialization(self):
        """ identity is properly initialized """
        identity = Pose()
        assert_almost_equal(identity.position, array([0, 0, 0]))
        assert_almost_equal(identity.attitude, array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
        
        self.assertRaises((TypeError, ValueError), Pose, position=1)
        self.assertRaises((TypeError, ValueError), Pose, position=[1, 2, 3, 4])
        self.assertRaises((TypeError, ValueError), Pose, attitude=[1, 2, 3, 4])

        self.assertTrue(isinstance(Pose(position=[0, 0]).position, ndarray))
        self.assertEqual(Pose(position=[0, 0]).position.shape, (3,))
        self.assertEqual(Pose(attitude=0).attitude.shape, (3, 3))

    def test_values(self):
        ''' Testing initialization with numpy scalar types '''
        Pose(position=[0, 0, 0], attitude=0)
        Pose(position=[0, 0, 0], attitude=numpy.float32(0))
        Pose(position=[0, 0, 0], attitude=numpy.float64(0))

    def testInit2(self):
        """ attitude can be initialized with 1d array """
        Pose([0, 0], array([0]))
        
  
    def testIdentity(self):
        """ Test that identity is neutral element """
        a = self.getRandom()
        b = self.getRandom()
        #c = self.getRandom()
        identity = Pose()
        D = a.oplus(b)
        self.assertSamePose(identity, identity)
        self.assertSamePose(identity, a.inverse().oplus(a))
        self.assertSamePose(identity, a.oplus(a.inverse()))
        self.assertSamePose(b, a.inverse().oplus(D))
        self.assertSamePose(a, D.oplus(b.inverse()))
         
    def assertSamePose(self, a, b):
        msg = " %s == %s (distance = %s ) " % (a, b, a.distance(b))
        self.assertTrue(a.__eq__(b), msg)    
    
        
