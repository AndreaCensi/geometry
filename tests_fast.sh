#!/bin/bash
set -e
set -x
nosetests --with-id -a '!density'  $* 