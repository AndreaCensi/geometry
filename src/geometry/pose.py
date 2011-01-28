from .common_imports import *

from .utils import rotz
from .rotations import  map_hat, hat_map
from .geometry_contracts import assert_allclose


#@contract(x='array[NxN]', returns='tuple(array[MxM],array[M],array[M],number),M=N-1')
def extract_pieces(x):
    M = x.shape[0] - 1
    a = x[0:M, 0:M]
    b = x[0:M, M]
    c = x[M, 0:M]
    d = x[M, M]
    return a, b, c, d

#@contract(a='array[MxM]', b='array[M]', c='array[M]', d='number', returns='array[NxN],N=M+1') 
def combine_pieces(a, b, c, d):
    M = a.shape[0]
    x = np.zeros((M + 1, M + 1)) 
    x[0:M, 0:M] = a
    x[0:M, M] = b
    x[M, 0:M] = c
    x[M, M] = d
    return x

@contract(R='array[NxN],orthogonal', t='array[N]',
          returns='array[MxM],M=N+1') # todo: sorthogonal
def pose_from_rotation_translation(R, t):
    return combine_pieces(R, t, t * 0, 1)
    
@contract(pose='array[NxN]', returns='tuple(array[MxM], array[M]),M=N-1')
def rotation_translation_from_pose(pose):
    R, t, zero, one = extract_pieces(pose)
    check('orthogonal', R)
    assert_allclose(one, 1)
    assert_allclose(zero, 0)
    return R, t



class Velocity:
    @contract(linear='array[3],finite', angular='array[3],finite')
    def __init__(self, linear, angular):
        self.linear = linear
        self.angular = angular
        
    @staticmethod
    @contract(V='array[4x4],finite')
    def from_matrix_representation(V):
        ''' Creates a Velocity object from its Lie algebra matrix representation.
          '''
        if not (V[3, :] == [0, 0, 0, 0]).all():
            raise ValueError('Malformed velocity %s' % str(V))
        angular = map_hat(V[0:3, 0:3])
        linear = V[0:3, 3]
        return Velocity(linear, angular)
    
    @contract(returns='array[4x4]')
    def to_matrix_representation(self):
        M = zeros((4, 4))
        M[0:3, 0:3] = hat_map(self.angular)
        M[0:3, 3] = self.linear
        return M
        
    def exponential(self):
        ''' Converts the velocity into the corresponding pose. '''
        M = self.to_matrix_representation()
        P = expm(M)
        return Pose.from_matrix_representation(P)
    
class Pose:
    ''' Objects of this class represent poses (position and attitude)
        in 3D (SE(3)). There are utility functions to extract 2D quantities 
        (position in R^2, attitude scalar = angle ). 
    '''
    def __init__(self, position=None, attitude=None):
        """ Initialize the object.
        
            Position can be:
            * None (-> [0,0,0] )
            * a list or vector (row or column) with 2 or 3 elements
            
            Attitude can be:
            * None (-> identity)
            * a float (2d orientation, interpreted as angle around z axis)
            * a (3,3) ndarray, interpreted as rotation matrix
            
            Other values will raise ValueError or TypeError.
        
            After initialization:
                 self.position is a (3,1) vector
                 self.attitude is a (3,3) vector 
        """
        if position == None:
            position = zeros(3)
        if attitude == None:
            attitude = eye(3)
            
        if not (isinstance(position, list) or isinstance(position, ndarray)):
            raise TypeError('Wrong type %s for position' % type(position))
        position = array(position).squeeze()
        if not (2 <= len(position) <= 3):
            raise ValueError('Wrong value %s for position' % position)
        if len(position) == 2:
            position = array([position[0], position[1], 0])
        
        # XXX: make this more general
        scalar_types = [float, int, float32, float64]
        ok_types = scalar_types + [ndarray]
        
        if not type(attitude) in ok_types:
            raise TypeError('Wrong type %s for attitude' % type(attitude))
        
        # XXX: make this more general
        if type(attitude) in scalar_types:
            attitude = rotz(float(attitude))
        elif isinstance(attitude, ndarray):
            if len(attitude) == 1:
                attitude = rotz(attitude.flatten()[0])
            elif not attitude.shape == (3, 3):
                raise ValueError('Bad shape for attitude: %s' % str(attitude.shape)) 
        # TODO: check that attitude is indeed a rotation matrix
        
        self.position = position 
        self.attitude = attitude 
        
    def get_2d_position(self):
        """ Get 2-vector corresponding to x,y components """
        self.assert2d()
        return self.position[0:2]
        
    def get_2d_orientation(self):
        """ Get angle corresponding to orientation """
        self.assert2d()
        forward = array([[1], [0], [0]])
        rotated = dot(self.attitude, forward)
        angle = arctan2(rotated[1, 0], rotated[0, 0])
        return float(angle)
        
    def assert2d(self):
        # TODO: implement this
        pass
        
    def oplus(self, that):
        """ Composition of two transformations. 
        
            Args:
                self:  the world->frame1 transformation
                that:  the frame1->frame2 transformation
            Returns:
                the world->frame2 transformation
                
            Example:
            
                vehicle_pose = ...
                sensor_pose = ...
                sensor_pose_world = vehicle_pose.oplus(sensor_pose)
        """
        if not isinstance(that, Pose):
            raise TypeError('Expected Pose, got %s', type(that))
        position = self.position + dot(self.attitude, that.position)
        attitude = dot(self.attitude, that.attitude)
        return Pose(position=position, attitude=attitude)
    
    def inverse(self):
        """ Returns the inverse transformation """
        attitude = self.attitude.transpose()
        position = -dot(attitude, self.position)
        return Pose(position=position, attitude=attitude)
    
    def distance(self, other): 
        if not isinstance(other, Pose):
            raise TypeError('Expected Pose, got %s', type(other))
        """ Returns a tuple containing the distance in (m, rad) between two configurations """
        T = dot(self.attitude.transpose(), other.attitude).trace() 
        C = (T - 1) / 2
        # make sure that |C| <= 1 (compensate numerical errors), otherwise arccos(1+eps) = nan
        if C > 1: 
            C = 1
        if C < -1:
            C = -1
        distance_rotation = arccos(C)
        distance_translation = norm(self.position - other.position)
        return (distance_rotation, distance_translation)
    
    def __eq__(self, other):
        distance_rotation, distance_translation = self.distance(other)
        tolerance_rotation = radians(0.0001)
        tolerance_translation = 0.0001
        return (distance_rotation < tolerance_rotation) and (distance_translation < tolerance_translation)
    
    def __str__(self):
        p = self.get_2d_position()
        r = degrees(self.get_2d_orientation())
        # TODO: output 3D if 3D
        return '<Pose pos=[%+.3fm %+.3fm] rot=%.2fdeg>' % (p[0], p[1], r)
        
    
    def get_xytheta(self):
        ''' Returns a numpy array containing (x,y,theta) 
        Raises an exception if this is a 3D pose. '''
        # TODO: make exception
        x, y = self.get_2d_position()
        theta = self.get_2d_orientation()
        return array([x, y, theta])

    def logarithm(self):
        ''' Returns the velocity corresponding to this pose. '''
        M = self.to_matrix_representation()
        V = logm(M)
        # Make sure that the result is real (it might be complex due
        # to numerical noise in M)
        V = array(V.real)
        # make the top 3,3 exactly skew
        V[0:3, 0:3] = 0.5 * (V[0:3, 0:3] - V[0:3, 0:3].transpose()) 
        # Make the last row exactly 0
        V[3, :] = 0
        
        return Velocity.from_matrix_representation(V) 
    
    # XXX: add some
    def to_matrix_representation(self):
        ''' Returns the matrix representation of this pose as 
            a 4 x 4 matrix. '''
        # matrix representation of this pose
        M = zeros((4, 4))
        M[0:3, 0:3] = self.attitude[:, :]
        M[0:3, 3] = self.position[:]
        M[3, 3] = 1
        return M
    
    @staticmethod
    # XXX @contract(A='pose',B='pose')
    def pose_diff(A, B):
        ''' Returns a pose X such that B.oplus(X) = A.
            Mnemonics: X = A - B '''
        # TODO: write unit tests for this
        return B.inverse().oplus(A)

    @staticmethod
    # XXX @contract(xytheta='seq[3](number)')
    def from_xytheta(xytheta):
        ''' Creates a Pose object from an iterable containing x,y,theta '''
        # TODO: write unit tests for this
        x, y, theta = xytheta
        return Pose(position=[x, y], attitude=theta)

    @staticmethod
    @contract(V='array[4x4],finite')
    def from_matrix_representation(V):
        ''' Creates a Pose object from its Lie algebra matrix representation.
              
        '''
        if not (V[3, :] == [0, 0, 0, 1]).all(): # XXX: 
            raise ValueError('Malformed pose matrix %s' % str(V))
        attitude = V[0:3, 0:3]
        check('rotation_matrix', attitude)
        position = V[0:3, 3]
        return Pose(position, attitude)
                        
                        
                        
