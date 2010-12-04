from numpy import pi, array, zeros
from numpy.random import randn, rand
from numpy.testing.utils import assert_almost_equal

from .. import Pose, Velocity
from .pose_tests import CompositionTests


def getRandom2DPose():
    return Pose(position=randn(2), attitude=rand(1) * pi)


class PoseAndVelTests(CompositionTests):
    
    def testIdentity(self):
        self.assertSamePose(Pose([0, 0], 0), \
                             Velocity(zeros(3), zeros(3)).exponential())
        
    def testConversions1(self):
        """ Testing conversions with exponential and logarithm """
        example_poses = [ Pose([0, 0], 0) ] + map(lambda i: getRandom2DPose(), range(5)) #@UnusedVariable
        for pose in example_poses: 
            velocity = pose.logarithm()
            pose2 = velocity.exponential()
            self.assertSamePose(pose, pose2)
           
    def testConversions2(self):
        """ Testing conversions with exponential and logarithm """
        example_velocities = [ Velocity(array([0, 0, 0]), array([0, 0, 0])),
                               Velocity(randn(3), randn(3)) ]
        for velocity in example_velocities: 
            pose = velocity.exponential()
            velocity2 = pose.logarithm()
            assert_almost_equal(velocity.to_matrix_representation(),
                                velocity2.to_matrix_representation())
        
        
