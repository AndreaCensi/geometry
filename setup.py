from setuptools import setup, find_packages

version = '1.4dev1'

setup(name='PyGeometry',
      version=version,
      author="Andrea Censi",
      author_email="acensi@idsc.mavt.ethz.ch",
      url='http://andreacensi.github.com/geometry/',
      license="LGPL",
      classifiers=[
        'Development Status :: 4 - Beta',
      ],
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=['PyContracts>=1.5,<2', 'numpy'],
      extras_require={
        'algorithms':  ["scipy"],
      },
      setup_requires=['nose>=1.0'],
      tests_require=['nose>=1.0', 'rudolf', 'nose-progressive', 'nose-cov'],
      download_url='http://github.com/AndreaCensi/geometry/tarball/%s' % version,
)
