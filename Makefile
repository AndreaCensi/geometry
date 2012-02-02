package=geometry

all: develop
	
develop:
	python setup.py develop

install:
	python setup.py install
	
docs: 
	make -C docs

nose=nosetests --with-id
nose_parallel=--processes=16 --process-timeout=30 --process-restartworker
nose_coverage=--with-coverage --cover-html --cover-html-dir coverage_information --cover-package=$(package) $(package)

test:
	@echo - Use "make test-failed" to redo only failed tests
	@echo - Use "make test-parallel" to enable parallel testing
	@echo - Use "make test-coverage" to do coverage testing
	@echo - Use NOSE_PARAMS to pass extra arguments.
	@echo
	$(nose) $(package)  -a '!density'  $(NOSE_PARAMS)

test-failed:
	$(nose) $(package)  -a '!density'  $(NOSE_PARAMS) --failed

test-parallel:
	$(nose) $(package) $(nose_parallel) $(NOSE_PARAMS)

test-coverage:
	@echo - Use NOSE_PARAMS to pass extra arguments.
	$(nose) $(package) $(nose_coverage) $(NOSE_PARAMS)

	