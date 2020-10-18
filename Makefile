package=geometry

include pypackage.mk



bump:
	bumpversion patch
	git push --tags
	git push --all

upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload dist/*

name=geometry-python3

test-python3:
	docker stop $(name) || true
	docker rm $(name) || true

	docker run -it -v "$(shell realpath $(PWD)):/geometry" -w /geometry --name $(name) python:3 /bin/bash

test-python3-install:
	pip install -r requirements.txt
	pip install nose
	python setup.py develop --no-deps



black:
	black -l 110 --target-version py37 src
