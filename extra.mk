.PHONY: docs test-circleci-local-staging upload-twine test-python3 test-python3-install

# The repository documentation uses its own docs.mk-based build.
docs:
	$(MAKE) -C docs

circleci-local-env = -e PIP_INDEX_URL=$(PIP_INDEX_URL) -e DOCKER_HUB_USERNAME=$(DOCKER_HUB_USERNAME) -e DOCKER_HUB_PASSWORD=$(DOCKER_HUB_PASSWORD)

test-circleci-local-staging:
	circleci local execute --job test-313-src $(circleci-local-env)

upload-twine:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload dist/*

python3-container-name = geometry-python3

test-python3:
	docker stop $(python3-container-name) || true
	docker rm $(python3-container-name) || true
	docker run -it -v "$(shell realpath $(PWD)):/geometry" -w /geometry --name $(python3-container-name) python:3 /bin/bash

test-python3-install:
	pip install -r requirements.txt
	pip install nose2
	python setup.py develop --no-deps
