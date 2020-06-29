PACKAGING
=========

This guide is loosely following one of Hynek's fantastic blog posts:

https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/


Note
----

This document is meant as a help for the maintainer only.


Preparation
-----------

- make sure changelog is up to date

- make sure the `long_description` can be rendered properly, ie. check with `longtest` (zest.releaser)

- make sure the version number is set correctly in `setup.py`

- make sure the version number is set correctly in `docs/conf.py`


Release process
---------------

    # create a development environment

    $ tox --devenv dev-env
    
    # install all necessary build tools

    $ dev-env/bin/pip install -U pip pep517 twine

    # make clean slate

    $ rm -rf build dist
 
    # build the packages

    $ dev-env/bin/python -m pep517.build .

    # make clean slate

    $ rm -rf venv-sdist

    # create a venv for the sdist installation test

    $ virtualenv venv-sdist

    # install package in sdist format

    $ venv-sdist/bin/pip install dist/Flask-Reuploaded-0.3.tar.gz  # swap version number

    # check the installed package

    $ venv-sdist/bin/python

    >>> import flask_uploads

    # make clean slate

    $ rm -rf venv-wheel

    # create a venv for the wheel installation test

    $ virtualenv venv-wheel

    # install the package in wheel format

    $ venv-wheel/bin/pip install dist/Flask_Reuploaded-0.3-py3-none-any.whl  # swap version number

    # check the installed packaged

    $ venv-wheel/bin/python

    >>> import flask_uploads

    # upload to test pypi

    $ twine upload -r test --sign dist/Flask*

    # upload to pypi

    $ twine upload -r pypi --sign dist/Flask*
