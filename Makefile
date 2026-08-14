all:
	@echo

out=out


template:
	zuper-cli template

bump:
	zuper-cli bump

upload:
	zuper-cli upload

black:
	black -l 110 --target-version py312 src

install-deps:
	pip3 install --user shyaml
	shyaml get-values install_requires < project.pp1.yaml > .requirements.txt
	pip3 install --user --upgrade -r .requirements.txt
	rm .requirements.txt

install-testing-deps:
	pip3 install --user shyaml
	shyaml get-values tests_require < project.pp1.yaml > .requirements_tests.txt
	pip3 install --user --upgrade -r .requirements_tests.txt
	rm .requirements_tests.txt

	pip install \
		pipdeptree\
		bumpversion\
		nose2\
		nose2-html-report\
		pre-commit\
		coverage\
		codecov\
		sphinx\
		sphinx-rtd-theme

test:
	DISABLE_CONTRACTS=1 python -m nose2 -v geometry_manifolds_tests geometry_tests

coverage-combine:
	coverage combine

docs:
	sphinx-build src $(out)/docs

-include extra.mk

# sigil 7b05953cf209480fb8535acd98dda778
