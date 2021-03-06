from setuptools import setup


def get_version():
    from pathlib import Path
    with open(Path(__file__).parent / "timefuncs" / "__init__.py") as file_:
        for line in file_.readlines():
            if line.startswith("__version__"):
                return line.split("\"")[1]


setup(
    name="timefuncs",
    version=get_version(),
    description="OWL TIME functions implemented as SPARQL extension functions in rdflib",
    long_description=open("README.md", encoding='utf-8').read(),
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
