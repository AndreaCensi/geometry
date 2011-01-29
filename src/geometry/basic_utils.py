from numpy import (cos, sin, sqrt, pi, zeros, array, eye, empty, clip) #@UnusedImport
from numpy import (dot, degrees, arccos, argmax, #@UnusedImport
                   vstack, hstack, sign, #@UnusedImport
                   ndarray, radians, float32, float64, arctan2, argmin)#@UnusedImport
from numpy.random import uniform #@UnusedImport
import numpy as np #@UnusedImport
from numpy.linalg import norm #@UnusedImport
from contracts import new_contract, check, contract #@UnusedImport
from scipy.linalg import logm, expm #@UnusedImport
from numpy.core.numeric import allclose
from numpy.linalg import  det, svd #@UnusedImport

import warnings

class Tolerance:
    zero_norm = 1e-7


def assert_allclose(actual, desired, rtol=1e-7, atol=0,
                    err_msg='', verbose=True):
    ''' Backporting assert_allclose from Numpy 1.5 to 1.4 '''
    from numpy.testing.utils import assert_array_compare
    def compare(x, y):
        return np.allclose(x, y, rtol=rtol, atol=atol)
    actual, desired = np.asanyarray(actual), np.asanyarray(desired)
    header = 'Not equal to tolerance rtol=%g, atol=%g' % (rtol, atol)
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
                         verbose=verbose, header=header)

@contract(s='array')
def normalize_length(s, norm=2):
    ''' Normalize an array such that it has unit length in the given norm. '''
    sn = np.linalg.norm(s, norm)
    if allclose(sn, 0, atol=Tolerance.zero_norm):
        raise ValueError('Norm is zero')
    else:
        return s / sn

@contract(s='array')
def normalize_length_or_zero(s, norm=2):
    ''' 
        Normalize an array such that it has unit length in the given norm; if the
        norm is close to zero, the zero vector is returned.     
    '''
    sn = np.linalg.norm(s, norm)
    if allclose(sn, 0, atol=Tolerance.zero_norm):
        return s
    else:
        return s / sn



@new_contract
@contract(x='array')
def finite(x):
    # TODO: make into standard thing
    return np.isfinite(x).all()

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    def new_func(*args, **kwargs):
        # TODO: mofify stack
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

def safe_arccos(x):
    ''' 
        Returns the arcosine of x, clipped between -1 and 1.
        
        Use this when you know x is a cosine, but it might be
        slightly over 1 or below -1 due to numerical errors.
    '''
    return arccos(clip(x, -1.0, 1.0))
