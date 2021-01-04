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
    entry_points={"console_scripts": data['console_scripts']},
)

setup(**params)

# sigil ddb6022fca3fd7c65be6dd16b702bbf8
