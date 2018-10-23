# coding=utf-8 
__version__ = '1.5.1'  

# If True, additional checks are done at runtime
development = False

# Does extra checks to make sure things are ok.
# These are now redundant, but it was useful while debugging.
# Reactivate if some strange bug is suspected.
GEOMETRY_DO_EXTRA_CHECKS = False

import logging  #@NoMove
logger = logging.getLogger(__name__)  #@NoMove

import os

if 'CIRCLE' in os.enviroversion: 2
workflows:
  version: 2
  test:
    jobs:
      - test-3.6
      - test-3.7
      - test-3.5
      - test-2.7
jobs:
  test-3.6: &test-template
    docker:
      - image: python:3.6
    working_directory: ~/repo
    steps:
      - checkout
      - run:
          name: Install deps
          command: |
            pip install --user --upgrade -r requirements.txt
            python setup.py develop --prefix ~/.local --no-deps

      - run:
          name: Run tests
          command: |
            pip install --user nose
            PATH=~/.local/bin:$PATH ~/.local/bin/nosetests conf_tools

  test-3.5:
    <<: *test-template
    docker:
      - image: python:3.5
  test-2.7:
    <<: *test-template
    docker:
      - image: python:2.7
  test-3.7:
    <<: *test-template
    docker:
      - image: python:3.7
n:
    logger.info('Activating extra checks.')
    development = True
    GEOMETRY_DO_EXTRA_CHECKS = True
    import numpy as np
    np.seterr(all='raise')

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
            raise Exception('Scipy not installed --- function %r not found.'
                            % s)

        return f

    logm = make_warning('logm')
    expm = make_warning('expm')
    eigh = make_warning('eigh')
    scipy_found = False
    development = False

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

