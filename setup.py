"""
Flask-Uploads
-------------
Flask-Uploads provides flexible upload handling for Flask applications. It
lets you divide your uploads into sets that the application user can publish
separately.

Links
`````
* `development version <https://github.com/svidela/flask-uploads>`_


"""
from setuptools import setup


setup(
    name="Flask-Uploads",
    version="0.2.1",
    url="https://github.com/svidela/flask-uploads",
    license="MIT",
    author="Santiago Videla",
    author_email="santiago.videla@gmail.com",
    description="Flexible and efficient upload handling for Flask",
    long_description=__doc__,
    py_modules=["flask_uploads"],
    zip_safe=False,
    platforms="any",
    install_requires=["flask>=1.1.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
