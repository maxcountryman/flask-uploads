How to contribute to this project
=================================

Thanks for considering to contribute!

Feel free to open issues for bug reports, feature requests and questions about this package.

Intended scope of this package
------------------------------

This package was created as the original `Flask-Uploads` stopped working back in February 2020.
At least the PyPi packages.

The intention is to provide a drop-in-replacement.

As I consider `Flask-Reuploaded` very stable and possibly feature complete,
big API changes are not intended.


How to contribute code
----------------------

Before you consider to contribute a big pull request,
please open an issue to discuss it beforehand.

When you are about to create a pull request,
please make sure all the tests are passing and the linters succeed.

You can run all checks with `tox <https://tox.readthedocs.io/en/latest/>`_.

Some examples.

	tox  # runs all checks

	tox -e py38  # runs the tests for Python 3.8

	tox -e flake8  # runs the Flake8 linter

If there is anything unclear, please feel free to ask!
