from contracts import contract

from . import MatrixLieGroup, np, MatrixLieAlgebra, SO, so, Euclidean

from geometry import  (assert_allclose,
                       pose_from_rotation_translation,
                           rotation_translation_from_pose,
                           extract_pieces, combine_pieces,
                        se2_from_SE2, SE2_from_se2, SE2_from_translation_angle)

class se(MatrixLieAlgebra):
    ''' This is the Lie algebra se(n) for the Special Euclidean group SE(n). 
    
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''
    
    def __init__(self, n, alpha):
        MatrixLieAlgebra.__init__(self, n)
        self.alpha = alpha
        self.son = so(n)
        
    def norm(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return np.linalg.norm(v) + self.alpha * self.son.norm(W)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        W = self.son.project(W)
        return combine_pieces(W, v, v * 0, 0)

    def __repr__(self):
        return 'se(%s)' % (self.n)
        

class SE(MatrixLieGroup):
    ''' 
        This is the Special Euclidean group SE(n) 
        describing roto-translations of Euclidean space.
        Implemented only for n=2,3.
        
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''
    
    @contract(n='int,(2|3)', alpha='>0')
    def __init__(self, n, alpha=1):
        algebra = se(n, alpha)
        MatrixLieGroup.__init__(self, n + 1, algebra)
        self.SOn = SO(n)
        self.En = Euclidean(n)
        
    def __repr__(self):
        return 'SE(%s)' % (self.n - 1)
    
    def belongs_(self, x):
        R, t, zero, one = extract_pieces(x) #@UnusedVariable
        self.SOn.belongs(R)
        assert_allclose(zero, 0, err_msg='I expect the lower row to be 0.') 
        assert_allclose(one, 1)

    def sample_uniform(self):
        t = self.En.sample_uniform()
        R = self.SOn.sample_uniform()
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
#        if False: #singularity
#            yield SE2_from_translation_angle([0, 0], -np.pi)
#            yield SE2_from_translation_angle([0, 0], +np.pi)
#            yield SE2_from_translation_angle([1, 0.1], -np.pi)
#            yield SE2_from_translation_angle([1, 0.1], +np.pi)
##        
#        for i in range(nrandom): #@UnusedVariable
#            t = np.random.rand(2)
#            theta = np.random.uniform(-1, 1) * np.pi
#            interesting.append(SE2_from_translation_angle(t, theta))
        
    
