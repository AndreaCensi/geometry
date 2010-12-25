from setuptools import setup

setup(name='snp-geometry',
      package_dir={'':'src'},
      packages=['snp_geometry'],
      install_requires=['numpy', 'scipy', 'PyContracts'] 
)

