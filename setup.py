import re
from setuptools import setup
from pathlib import Path


def get_version():
    with open(Path(__file__).parent / "CHANGELOG.md") as file_:
        return file_.readlines()[0]


def get_long_description():
    return open("README.md", encoding='utf-8').read()


setup(
    name="timefuncs",
    version=get_version(),  # __import__("timefuncs").__version__,
    description="OWL TIME functions implemented as SPARQL extension functions in rdflib",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    maintainer="Nicholas J. Car",
    maintainer_email="nicholas.car@anu.edu.au",
    url="https://github.com/rdflib/timefuncs",
    license="BSD",
    packages=["timefuncs"],
    platforms=["any"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    test_suite="tests",
    install_requires=["rdflib>=6.0.0"],
    tests_require=["pytest"],
)
