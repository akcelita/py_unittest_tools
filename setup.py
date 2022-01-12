from setuptools import setup
import os.path
import json


with open(os.path.join(os.path.dirname(__file__), "package.json")) as finp:
    package = json.load(finp)


setup(
    name=package['name'],
    python_requires=package['python_version'],
    version=package['version'],
    description=package['description'],
    url=package['repository']['url'],
    author=package['author']['name'],
    author_email=package['author']['email'],
    packages=['py_unittest_tools'],
    install_requires=package['python_dependencies'],
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
