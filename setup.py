from setuptools import setup


setup(name='PyGeometry',
      version='0.9.1',
      package_dir={'':'src'},
      packages=['geometry', 'geometry.manifolds'],
      install_requires=['numpy', 'scipy', 'PyContracts'] 
)

