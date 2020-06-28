.. image:: https://travis-ci.com/jugmac00/flask-reuploaded.svg?branch=master
    :target: https://travis-ci.com/jugmac00/flask-reuploaded

.. image:: https://coveralls.io/repos/github/jugmac00/flask-reuploaded/badge.svg?branch=master
    :target: https://coveralls.io/github/jugmac00/flask-reuploaded?branch=master

.. image:: https://img.shields.io/pypi/v/flask-reuploaded   
    :alt: PyPI
    :target: https://github.com/jugmac00/flask-reuploaded


Flask-Reuploaded
================

Flask-Reuploaded provides file uploads for Flask.


Notes on this package
---------------------

This is an independently maintained version of `Flask-Uploads` based
on the 0.2.1 version of the original, but also including four years of
unreleased changes - at least not released to PyPi.

Noteworthy is the fix for the `Werkzeug` API change.


Goals
-----

- `Flask-Reuploaded` is a stable drop-in replacement for `Flask-Uploads`
- regain momentum for this widely used package
- provide working PyPi packages


Migration guide from `Flask-Uploads`
------------------------------------

If you have used `Flask-Uploads` and want to migrate to `Flask-Reuploaded`,
you only have to install `Flask-Reuploaded` instead of `Flask-Uploads`.

That's all!

So, if you use `pip` to install your packages, instead of ...

    $ pip install `Flask-Uploads`  # don't do this! package is broken

... just do ...

    $ pip install `Flask-Reuploaded`

`Flask-Reuploaded` is a drop-in replacement.

This means you do not have to change a single line of code.


Contributing
------------

Contributions are more than welcome. Please have a look at
https://github.com/jugmac00/flask-reuploaded/issues


Installation
------------

    $ pip install Flask-Reuploaded
