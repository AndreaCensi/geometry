# Template v. 1.6
package=geometry
demos_root=source/my_static/demos
github_repo=git@github.com:AndreaCensi/geometry.git

# also change this in epydoc.cfg
webdir=website
webgit=git --git-dir $(webdir)/.git --work-tree=$(webdir)/ 

all: compile-website 
	
compile-website: website epydoc
	PYTHONPATH=`pwd`:$(PYTHONPATH) sphinx-build -E -n -a -b html source $(webdir)

compile:
	PYTHONPATH=`pwd`:$(PYTHONPATH) sphinx-build -n -a -b html source $(webdir)
	
website: distclean
	# Check out the website
	git clone $(github_repo) $@
	$(webgit) checkout origin/gh-pages -b gh-pages
	$(webgit) branch -D master

upload:
	$(webgit) commit -m "updated website" -a 
	$(webgit) push

distclean:
	rm -rf $(webdir)/
	
epydoc:
	epydoc --config epydoc.cfg --introspect-only -v --exclude-introspect=$(package).unittests --debug
