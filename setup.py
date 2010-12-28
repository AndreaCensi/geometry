from setuptools import setup

setup(name='snp-geometry',
      version='0.9',
      package_dir={'':'src'},
      packages=['snp_geometry'],
      install_requires=['numpy', 'scipy', 'PyContracts'] 
)

