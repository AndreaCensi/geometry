from . import DifferentiableManifold, MatrixLieGroup, np, SO, se, R
from .. import (assert_allclose, pose_from_rotation_translation,
    rotation_translation_from_pose, extract_pieces, se2_from_SE2, SE2_from_se2,
    SE2_from_translation_angle, SE2_from_xytheta)
from contracts import contract
from contracts.interface import describe_value


class SE_group(MatrixLieGroup):
    ''' 
        This is the Special Euclidean group SE(n) 
        describing roto-translations of Euclidean space.
        Implemented only for n=2,3.
        
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''
    
    @contract(N='int,(2|3)')
    def __init__(self, N):
#        print('Instantiating SE%s' % N)
        algebra = se[N]
        self.SOn = SO[N]
        self.En = R[N]
        dimension = {2:3, 3:6}[N]
        MatrixLieGroup.__init__(self, n=N + 1, algebra=algebra, dimension=dimension)
        
        DifferentiableManifold.embedding(self, algebra,
                                          self.algebra_from_group,
                                    self.group_from_algebra,
                                    type='lie')

    def __repr__(self):
        #return 'SE(%s)' % (self.n - 1)
        return 'SE%s' % (self.n - 1)
    
    def belongs_(self, x):
        R, t, zero, one = extract_pieces(x) #@UnusedVariable
        self.SOn.belongs(R)
        assert_allclose(zero, 0, err_msg='I expect the lower row to be 0.') 
        assert_allclose(one, 1)

    def sample_uniform(self):
        t = self.En.sample_uniform()
        R = self.SOn.sample_uniform()
        assert t.size == R.shape[0]
        return pose_from_rotation_translation(R, t)
            
    def friendly(self, x):
        R, t = rotation_translation_from_pose(x)
        return 'Pose(%s,%s)' % (self.SOn.friendly(R), self.En.friendly(t))
    
    # TODO: make explicit inverse
    # TODO: make specialization for SE(3)
    def logmap_(self, base, target):
        ''' Uses special form for logarithmic map. '''
        if self.n == 3:
            diff = self.multiply(self.inverse(base), target)
            X = se2_from_SE2(diff)            
            X = self.algebra.project(X)
            return np.dot(base, X)
        else:
            return MatrixLieGroup.logmap_(self, base, target)
    
    def expmap_(self, base, vel):
        ''' Uses special form for exponential map. '''
        if self.n == 3:
            tv = np.dot(self.inverse(base), vel)
            tv = self.algebra.project(tv)
            x = SE2_from_se2(tv)
            return np.dot(base, x)
        else: #
            return MatrixLieGroup.expmap_(self, base, vel)

        
    def interesting_points(self):
        if self.n == 3:
            interesting = [
                SE2_from_translation_angle([0, 0], 0),
                SE2_from_translation_angle([0, 0], 0.1),
                SE2_from_translation_angle([0, 0], -0.1),
                SE2_from_translation_angle([1, 0.1], 0),
            ]
        else:
            # TODO: implement for SE3
            interesting = []
        return interesting

    def from_yaml(self, value):
        ''' Parses from yaml value. '''
        if self.n == 3: # SE2
            x = np.array(value)
            if x.shape != (3,):
                msg = 'I expect a 3-array, not %s' % describe_value(value)
                raise ValueError(msg)
            return SE2_from_xytheta(x) 
        else:
            raise ValueError('Not implemented in %r' % self.__class__.__name__)
            


