import json

from setuptools import setup

with open("setup.json") as f:
    data = json.load(f)

# setup package
params = dict(
    name=data['package_name'],
    author=data["author"],
    author_email=data["author_email"],
    url=data["url"],
    tests_require=data['tests_require'],
    install_requires=data['install_requires'],
    package_dir={"": data['srcdir']},
    packages=data['modules'],
    long_description="",
    version=data['version'],
    entry_points=data['entry_points'],
    zip_safe=data['zip_safe'],
    include_package_data=data['include_package_data'],
)

setup(**params)

# sigil 785edf5fce85417b0c8d4297bedddf78
