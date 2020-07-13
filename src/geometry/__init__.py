# coding=utf-8
__version__ = "2.0.1"

# If True, additional checks are done at runtime
development = False

# Does extra checks to make sure things are ok.
# These are now redundant, but it was useful while debugging.
# Reactivate if some strange bug is suspected.
GEOMETRY_DO_EXTRA_CHECKS = False


def create_logger():
    import logging

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger


logger = create_logger()


def in_circle():
    import os

    return "CIRCLE" in os.environ


def set_numpy_errors_to_raise():
    import numpy as np

    np.seterr(all="raise")


if in_circle():
    logger.info("Activating extra checks.")
    development = True
    GEOMETRY_DO_EXTRA_CHECKS = True
    set_numpy_errors_to_raise()

try:
    from scipy.linalg import logm, expm, eigh

    scipy_found = True
except ImportError:
    msg = "Scipy not found -- needed for functions logm, expm, eigh. "
    msg += "I will go on without it, but later an error will be thrown "
    msg += "if those functions are used."

    logger.warn(msg)

    def make_warning(s):
        def f(*args, **kwargs):
            raise Exception("Scipy not installed --- function %r not found." % s)

        return f

    logm = make_warning("logm")
    expm = make_warning("expm")
    eigh = make_warning("eigh")
    scipy_found = False
    development = False

from .types import *
from .basic_utils import *
from .constants import *
from .distances import *
from .formatting import *
from .manifolds import *
from .mds_algos import *
from .poses import *
from .poses_embedding import *
from .procrustes import *
from .rotations import *
from .rotations_embedding import *
from .spheres import *
from .spheres_embedding import *
