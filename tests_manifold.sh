#!/bin/bash
set -e
set -x
nosetests -a 'manifolds'  $*
