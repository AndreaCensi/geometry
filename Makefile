package=geometry

include pypackage.mk



bump-upload:
	bumpversion patch
	git push --tags
	git push --all
	rm -f dist/*
	python setup.py sdist
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

