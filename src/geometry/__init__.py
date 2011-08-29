__version__ = '0.12.0dev'
# If True, additional checks are done at runtime
development = True

# If you want to be safe
# import numpy as np
# np.seterr(all='err')
try:
    from scipy.linalg import logm, expm, eigh
    scipy_found = True
except ImportError:
    msg = 'Scipy not found -- needed for functions logm, expm, eigh. '
    msg += 'I will go on without it, but later an error will be thrown '
    msg += 'if those functions are used.'
    import warnings
    warnings.warn(msg)
    def make_warning(s):
        def f(*args, **kwargs):
            raise Exception('Scipy not installed --- function %r not found.' % s)
        return f
    logm = make_warning('logm')
    expm = make_warning('expm')
    eigh = make_warning('eigh')
    scipy_found = False

if not scipy_found:
    development = False

from .formatting import *
from .basic_utils import *
from .spheres import *
from .spheres_embedding import * 
from .rotations import *
from .rotations_embedding import *  
from .poses import *
from .poses_embedding import *
from .procrustes import *
from .manifolds import *
from .mds_algos import *

