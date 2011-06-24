from setuptools import setup

version='0.9.7'

setup(name='PyGeometry',
      version=version,
      author="Andrea Censi",
      author_email="andrea@cds.caltech.edu",
      url='http://andreacensi.github.com/geometry/',
      license="LGPL",
      classifiers=[
        'Development Status :: 4 - Beta',
      ],
      package_dir={'':'src'},
      packages=['geometry', 'geometry.manifolds'],
      install_requires=['PyContracts'],
     download_url='http://github.com/AndreaCensi/geometry/tarball/%s' % version,

)
