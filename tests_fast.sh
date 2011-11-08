#!/bin/bash
set -e
set -x
nosetests --with-id --progressive -a '!density' -w src $*