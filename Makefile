package=geometry

include pypackage.mk



bump:
	bumpversion patch
	git push --tags
	git push --all

env=-e PIP_INDEX_URL=$(PIP_INDEX_URL) -e DOCKER_HUB_USERNAME=$(DOCKER_HUB_USERNAME) -e DOCKER_HUB_PASSWORD=$(DOCKER_HUB_PASSWORD)

test-circleci-local-staging:
	circleci local execute --job test-3.8-staging $(env)

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
