all: develop
	
develop:
	python setup.py develop

install:
	python setup.py install
	
test: test-fast
	
test-fast:
	nosetests  --with-id -a '!density'  geometry
	
test-manifold:
	nosetests  --with-id -a 'manifolds'  geometry
	
test-coverage:
	nosetests --with-doctest --with-coverage --cover-html --cover-html-dir coverage_information --cover-package=geometry geometry
	