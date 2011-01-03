from numpy import  isfinite, dot
import numpy
from numpy.testing.utils import assert_almost_equal

class gt:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return other > self.n
    
    def __str__(self):
        return '>%s' % self.n 

class square_shape:
    def __eq__(self, other):
        return len(other) == 2  and other[0] == other[1] 

def require_array_with_shape(v, expected_shape):
    require_array(v)
    if not expected_shape == v.shape:
        raise ValueError('Expecting shape %s, got %s' % 
                         (expected_shape, v.shape))  
        
def require_square(v):
    require_array_with_shape(v, square_shape())


def require_array(v):
    if not isinstance(v, numpy.ndarray):
        raise ValueError('Expecting a numpy array, got %s.' % 
                         v.__class__.__name__)

def require_finite(a):
    ''' Checks that there are no NaNs or Inf in the array. '''
    require_array(a)
    if not isfinite(a).all():
        raise ValueError('Invalid value %s' % a)

def require_length(a, length):
    ''' Checks that a is a numpy array that can be cast to 
        an iterable of given length. '''
    require_array(a)
    if len(a) != length:
        raise ValueError('Expecting something of length %s, got %s which has len %s' % 
                         (length, a.shape, len(a)))  
    
    
def require_skew_symmetric(a):
    require_array_with_shape(a, square_shape())
    diag = a.diagonal()
    if not (diag == 0).all():
        raise ValueError('Expected skew symmetric, but diagonal is %s.' % diag)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if i < j:
                if a[i, j] != -a[j, i]:
                    raise ValueError('Expected skew symmetric, but ' + 
                                     'a[%d][%d] = %f, a[%d][%d] = %f' % \
                                     (i, j, a[i, j], j, i, a[j, i]))
    
def require_orthogonal(R):
    require_square(R)
    Id1 = dot(R.transpose(), R)
    Id2 = dot(R, R.transpose())
    Id = numpy.eye(R.shape[0])
    assert_almost_equal(Id1, Id)
    assert_almost_equal(Id2, Id)
    
        
    
    
    
    
