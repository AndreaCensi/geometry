#!/bin/bash
set -e
set -x
nosetests -a '!density' -w src $*