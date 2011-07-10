from . import DifferentiableManifold, contract

def NonCompactStiefel(DifferentiableManifold):
    ''' INCOMPLETE -- Matrices of fixed rank. '''
    
    @contract(n='N,N>0', p='P,P>0,P<=N')
    def __init__(self, p, n):
        ''' 
            Initializes the manifold structure. 
            
            :param n: dimension of space
            :param p: rank of subspace
        '''
        DifferentiableManifold.__init__(self)
        self.n = n
        self.p = p

    def belongs_(self, a):
        assert False

    def distance_(self, a, b):
        assert False

    def logmap_(self, a, b): 
        assert False

    def expmap_(self, a, vel): 
        assert False

    def project_ts_(self, base, vx): 
        assert False
    
    def sample_uniform(self):
        assert False
    
    def normalize(self, x):
        assert False
        
def Grassman(DifferentiableManifold):
    ''' 
        INCOMPLETE -- The Grassman manifold Grass(n,p) is the set of rank-p 
        subspaces in R^n. It is seen here as Grass(n,p) = ST(n,p)/GL_p.
    
        For a reference, see the paper by Absil, Mahony, and Sepulchre (2004)
        where all these operations are explained. Also their book should
        contain essentially the same info, but with more background.
        
    '''
    @contract(n='N,N>0', p='P,P>0,P<=N')
    def __init__(self, p, n):
        ''' 
            Initializes the manifold structure. 
            
            :param n: dimension of space
            :param p: rank of subspace
        '''
        self.n = n
        self.p = p

    def belongs_(self, a):
        assert False

    def distance_(self, a, b):
        assert False

    def logmap_(self, a, b): 
        assert False

    def expmap_(self, a, vel): 
        assert False

    def project_ts_(self, base, vx): 
        assert False
    
    def sample_uniform(self):
        assert False
    
    def normalize(self, x):
        assert False

