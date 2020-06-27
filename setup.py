# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return the contents of the read file.

    - Build an absolute path from *parts*
    - Return the contents of the resulting file.
    - Assume UTF-8 encoding.

    Proudly copy-pasted from Hynek's attrs project
    (minus the typo).
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


LONG = read("README.rst") + "\n\n" + read("CHANGES.rst")

setup(
    name="Flask-Reuploaded",
    version="0.3",
    url="https://github.com/jugmac00/flask-reuploaded",
    license="MIT",
    author='Matthew "LeafStorm" Frazier',
    author_email="leafstormrush@gmail.com",
    maintainer="Jürgen Gmach",
    maintainer_email="juergen.gmach@googlemail.com",
    description="Flexible and efficient upload handling for Flask",
    long_description=LONG,
    py_modules=["flask_uploads"],
    zip_safe=False,
    platforms="any",
    install_requires=["Flask>=1.0.4"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Flask",
    ],
)
